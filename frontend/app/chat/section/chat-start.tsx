import { Button, Input } from "antd"
import { redirect } from "next/navigation"
import { Dispatch, SetStateAction, useState } from "react"

export default ({sendMsg}: {
  sendMsg: (msg: string) => void
}) => {
  const [currentMsg, setCurrentMsg] = useState('')
  return (
    <div className="min-w-1/2 my-auto mx-auto self-center text-center">
      <span className="text-2xl">从哪里开始呢</span>
      <div className="input flex mt-4">
        <Input placeholder="有问题，尽管问" value={currentMsg} onChange={(e) => setCurrentMsg(e.target.value)} onPressEnter={() => sendMsg(currentMsg)}></Input>
        <div className="btn">
          <Button onClick={() => sendMsg(currentMsg)}>发送</Button>
        </div>
      </div>
    </div>
  )
}