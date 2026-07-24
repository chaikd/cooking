import { Button } from "antd"
import { useRef } from "react"
import ChatInput from "./chat-input"

export default ({sendMessage}: {
  sendMessage: (msg: string) => void
}) => {
  const chatInputRef = useRef<{
    getCurrentMsg: () => string
  }>(null)
  return (
    <div className="min-w-1/2 self-center text-center p-4">
      <span className="text-2xl">从哪里开始呢</span>
      <div className="input flex mt-4">
        <ChatInput sendMessage={sendMessage} ref={chatInputRef}></ChatInput>
        <div className="btn">
          <Button onClick={() => sendMessage(chatInputRef?.current?.getCurrentMsg() || '')}>发送</Button>
        </div>
      </div>
    </div>
  )
}