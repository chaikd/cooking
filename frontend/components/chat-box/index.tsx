"use client"
import { Button } from "antd"
import ChatStart from "./chat-start"
import classNames from "classnames"
import { useRef } from "react"
import ChatInput from "./chat-input"

export interface ChatMessageInfo {
  createTime: Date | string;
  message: string;
  type: 'user' | 'ai' | 'aiThinking';
}

export default ({
  isStart = false,
  messages = [],
  sendMessage
}: {
  isStart?: boolean,
  messages: Array<ChatMessageInfo>,
  sendMessage: (msg: string) => void
}) => {
  console.log("🚀 ~ messages:", messages)
  const chatInputRef = useRef<{
    getCurrentMsg: () => string
  }>(null)
  if(isStart) {
    return <div className="h-full flex items-center justify-center">
      <ChatStart sendMessage={sendMessage}/>
    </div>
  }
  return <div className="chat-box max-w-[640px] mx-auto h-full flex flex-col p-2">
    <div className="flex-1 h-0 overflow-y-auto">
      {
        messages?.length && messages.map((v: ChatMessageInfo) => {
          return <div className={classNames(
            (v.type === 'user' ? 'float-right max-w-[300px] p-2 rounded bg-blue-200' : ''),
          )}>{v.message}</div>
        }) || '输入内容，发起聊天'
      }
    </div>
    <div className="flex">
      <ChatInput sendMessage={sendMessage} ref={chatInputRef}></ChatInput>
      <div className="ml-2">
        <Button onClick={() => sendMessage(chatInputRef.current?.getCurrentMsg() || '')}>发送</Button>
      </div>
    </div>
  </div>
}