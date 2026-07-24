"use client"
import { redirect } from "next/navigation"
import { sendMessage } from "@/services/api/session"
import ChatBox, { ChatMessageInfo } from "@/components/chat-box"
import { useEffect, useRef, useState } from "react"
import { message } from "antd"
import moment from "moment"

export default ({
  id
}: {
  id: string
}) => {
  console.log("🚀 ~ id:", id)
  const messagesRef = useRef<Array<ChatMessageInfo>>([])
  const [messages,setMessages] = useState<Array<ChatMessageInfo>>([])
  const sendMessageFn = (msg: string) => {
    if(msg) {
      messagesRef.current = messagesRef.current.concat({
        type: 'user',
        message: msg,
        createTime: moment(new Date().getTime()).format('YYYY-MM-dd HH:mm:ss')
      })
      console.log("🚀 ~ sendMessageFn ~ newMessages:", messagesRef.current)
      setMessages(messagesRef.current)
    } else {
      message.warning('请输入')
      return
    }
    console.log("🚀 ~ sendMessageFn ~ msg:", msg)
    const uuid = crypto.randomUUID()
    redirect(`/chat/${uuid}`)
    // sendMessage({
    //   type: 'text',
    //   message,
    //   id: uuid
    // }).then(res => {
    //   console.log('res',res)
    //   redirect(`/chat/${uuid}`)
    // })
  }
  useEffect(() => {
    setMessages(messagesRef.current)
  })
  return <ChatBox messages={messages} isStart={!id} sendMessage={sendMessageFn}></ChatBox>
}