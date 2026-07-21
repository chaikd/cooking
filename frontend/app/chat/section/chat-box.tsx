"use client"
import { Button, Input, Space } from "antd"
import ChatStart from "./chat-start"
import { redirect } from "next/navigation"
import { sendMessage } from "@/services/api/session"

export default ({id}: {id?: string}) => {
  const sendMsg = (message: string) => {
    const uuid = crypto.randomUUID()
    sendMessage({
      type: 'text',
      message,
      id: uuid
    }).then(res => {
      console.log('res',res)
      redirect(`/chat/${uuid}`)
    })
  }
  if(!id) {
    return <ChatStart sendMsg={sendMsg}/>
  }
  return <div className="chat-box max-w-[640px] mx-auto h-full flex flex-col p-2">
    <div className="flex-1 h-0 ">
      内容
    </div>
    <div className="input flex">
      <Input></Input>
      <div className="btn">
        <Button>发送</Button>
      </div>
    </div>
  </div>
}