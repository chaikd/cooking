"use client"
import { Button } from "antd"
import ChatStart from "./chat-start"
import classNames from "classnames"
import { useEffect, useRef } from "react"
import ChatInput from "./chat-input"
import { redirect } from "next/navigation"
import { Streamdown as Markdown } from "streamdown"
import { code } from "@streamdown/code";
import { mermaid } from "@streamdown/mermaid";
import { math } from "@streamdown/math";
import { cjk } from "@streamdown/cjk";

export interface ChatMessageInfo {
  id: string;
  createTime: Date | string;
  message: string;
  role: 'user' | 'assistant' | 'aiThinking';
  conversationId?: string
}

export default ({
  isStart = false,
  messages = [],
  disabled = false,
  sendMessage
}: {
  isStart?: boolean,
  disabled?: boolean,
  messages: Array<ChatMessageInfo>,
  sendMessage: (msg: string) => void
}) => {
  const boxRef = useRef<HTMLDivElement | null>(null)
  const chatInputRef = useRef<{
    getCurrentMsg: () => string;
    initMsg: () => void;
  }>(null)
  const sendMessageFn = (msg: string) => {
    sendMessage(msg)
    chatInputRef.current?.initMsg()
  }
  useEffect(() => {
    boxRef.current?.scrollTo({
      top: boxRef.current?.scrollHeight
    })
  }, [messages])
  if(isStart) {
    return <div className="h-full flex items-center justify-center">
      <ChatStart sendMessage={sendMessageFn}/>
    </div>
  }
  return <div className="chat-box max-w-[640px] mx-auto h-full flex flex-col p-2">
    <div className="flex-1 h-0 overflow-y-auto" ref={boxRef}>
      {
        messages?.length && messages.map((v: ChatMessageInfo) => {
          return <div key={v.id} className={classNames(
            (v.role === 'user' ? 'text-right' : ''),
          )}>
            {
              v.role === 'user' 
                ? <span className={classNames(
                  v.role === 'user' ? 'inline-block max-w-[300px] p-2 rounded bg-blue-200' : ''
                )}>{v.message}</span>
                : <div className="mt-2">
                  <Markdown plugins={{ code, mermaid, math, cjk }}>{v.message}</Markdown>
                </div>
            }
          </div>
        }) || <span onClick={() => redirect('/chat')}>输入内容，发起聊天</span>
      }
    </div>
    <div className="flex mt-4">
      <ChatInput sendMessage={sendMessageFn} ref={chatInputRef}></ChatInput>
      <div className="ml-2">
        <Button disabled={disabled} onClick={() => {
          sendMessageFn(chatInputRef.current?.getCurrentMsg() || '');
        }}>发送</Button>
      </div>
    </div>
  </div>
}