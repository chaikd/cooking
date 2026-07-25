"use client"
import ChatBox, { ChatMessageInfo } from "@/components/chat-box"
import { message } from "antd"
import moment from "moment"

export default ({
  id,
  messages,
  setMessages,
  onSendNewMessage
}: {
  id: string,
  messages: ChatMessageInfo[],
  setMessages: (messages: any) => void,
  onSendNewMessage: (messageInfo: any) => void
}) => {
  const sendMessageFn = (msg: string) => {
    if(msg) {
      const currentMessage = {
        type: 'user',
        message: msg,
        createTime: moment(new Date().getTime()).format('YYYY-MM-dd HH:mm:ss')
      }
      setMessages([currentMessage])
      const uuid = crypto.randomUUID()
      onSendNewMessage({
        ...currentMessage,
        convasitionId: uuid,
        id: crypto.randomUUID()
      })
    } else {
      message.warning('请输入')
      return
    }
    
    // redirect(`/chat/${uuid}`)
    // sendMessage({
    //   type: 'text',
    //   message,
    //   id: uuid
    // }).then(res => {
    //   console.log('res',res)
    //   redirect(`/chat/${uuid}`)
    // })
  }
  return <ChatBox messages={messages} isStart={!id} sendMessage={sendMessageFn}></ChatBox>
}