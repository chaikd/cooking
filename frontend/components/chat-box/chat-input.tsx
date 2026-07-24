import { Input } from "antd"
import { forwardRef, useImperativeHandle, useState } from "react"

export default forwardRef(({sendMessage}: {
  sendMessage: (msg: string) => void
}, ref) => {
  const [currentMsg, setCurrentMsg] = useState('')
  useImperativeHandle(ref, () => ({
    getCurrentMsg: () => currentMsg
  }))
  return <Input placeholder="有问题，尽管问" value={currentMsg} onChange={(e) => setCurrentMsg(e.target.value)} onPressEnter={() => sendMessage(currentMsg)}></Input>
})