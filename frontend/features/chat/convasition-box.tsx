"use client"
import ChatBox, { ChatMessageInfo } from "@/components/chat-box"
import { getMessages, sendMessage } from "@/services/api/session"
import { message } from "antd"
import moment from "moment"
import { useEffect, useState } from "react"

export default ({
  id,
  onSendNewMessage
}: {
  id: string,
  onSendNewMessage: (messageInfo: any) => void
}) => {
  const [messages,setMessages] = useState<ChatMessageInfo[]>([])
  const [chatDisabled, setChatDisabled] = useState<boolean>(false)
  const sendMessageFn = (msg: string) => {
    if(msg) {
      const currentMessage: ChatMessageInfo = {
        role: 'user',
        message: msg,
        createTime: moment(new Date().getTime()).format('YYYY-MM-dd HH:mm:ss'),
        conversationId: id || crypto.randomUUID(),
        id: crypto.randomUUID()
      }
      if (!id) {
        localSave([currentMessage])
        onSendNewMessage({
          ...currentMessage,
        })
      }
      setMessages([...messages, currentMessage])
      if (id) {
        fetchMessage({
          ...currentMessage
        })
      }
    } else {
      message.warning('请输入')
      return
    }
  }
  const localSave = (newMessages: ChatMessageInfo[]) => {
    if(!id && !messages?.length) {
      localStorage.setItem('messages', JSON.stringify(newMessages))
    }
  }
  const fetchMessage = async (messageInfo: any) => {
    setChatDisabled(true)
    try {
      const stream = await sendMessage({
        type: 'text',
        message: messageInfo.message,
        id: messageInfo.conversationId
      })
      if (!stream) return

      const reader = stream.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      // 先添加一条空的 ai 消息，后续流式填充
      const assistantMessage: ChatMessageInfo = {
        id: crypto.randomUUID(),
        role: 'assistant',
        message: '',
        createTime: moment(new Date().getTime()).format('YYYY-MM-dd HH:mm:ss')
      }
      setMessages((prev: ChatMessageInfo[]) => [...prev, assistantMessage])

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        // 保留末尾不完整的行，下次读取时拼接
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (!line.trim()) continue

          // 解析 SSE 事件
          if (line.startsWith('event: ')) {
            const eventType = line.slice(7).trim()
            // 收到 done 事件，流结束
            if (eventType === 'done') {
              reader.cancel()
              return
            }
          }

          if (line.startsWith('data: ')) {
            const raw = line.slice(6)
            if (raw === '[DONE]') {
              reader.cancel()
              return
            }
            // ServerSentEvent 会把 data 做 JSON 编码（Unicode 转义），
            // 需要 JSON.parse 解码回原始字符串
            const data = JSON.parse(raw) as string
            // 更新最后一条 ai 消息的内容
            setMessages((prev: ChatMessageInfo[]) => {
              const updated = [...prev]
              const last = updated[updated.length - 1]
              if (last && last.role === 'assistant') {
                updated[updated.length - 1] = {
                  ...last,
                  message: last.message + data
                }
              }
              return updated
            })
          }
        }
      }
    } catch (err: any) {
      // 流被中断（如 reader.cancel()）不算错误
      if (err?.name === 'AbortError') return
      console.error('Stream error:', err)
    } finally {
      setChatDisabled(false)
    }
  }
  const getMessageList = async (sessionId: string) => {
    const res = await getMessages(sessionId)
    setMessages(res)
  }
  useEffect(() => {
    if(id && !messages?.length) {
      const messages = localStorage.getItem('messages')
      if(messages) {
        const parseMessages = JSON.parse(messages)
        setMessages(parseMessages)
        localStorage.removeItem('messages')
        if(parseMessages.length === 1)  {
          fetchMessage(parseMessages[0])
        }
      } else {
        getMessageList(id)
      }
    }

  })
  return <ChatBox disabled={chatDisabled} messages={messages} isStart={!id} sendMessage={sendMessageFn}></ChatBox>
}