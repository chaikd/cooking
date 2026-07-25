"use client"
import { ChatMessageInfo } from "@/components/chat-box"
import ConvasitionBox from "@/features/chat/convasition-box"
import ConvasitionList, { ConvasitionListItemType } from "@/features/chat/convasition-list"
import { useEffect, useState } from "react"

export default ({id, listData}: {
  id: string,
  listData: ConvasitionListItemType[]
}) => {
  const [messages,setMessages] = useState<ChatMessageInfo[]>([])
  const [listDataState, setListDataState] = useState<ConvasitionListItemType[]>(listData)
  const sendNewMessage = (
    messageInfo: any
  ) => {
    const newMessages = [...messages, messageInfo]
    const newListData = [{
      id: messageInfo.convasitionId,
      title: messageInfo.message
    }, ...listData]
    localSave(newMessages, newListData)
    setMessages(newMessages)
    setListDataState(newListData)
  }
  const localSave = (newMessages: ChatMessageInfo[], newListData: ConvasitionListItemType[]) => {
    if(!id && (!messages?.length || !listData?.length)) {
      localStorage.setItem('messages', JSON.stringify(newMessages))
      localStorage.setItem('listData', JSON.stringify(newListData))
    }
  }
  useEffect(() => {
    if(id && !messages?.length && !listData?.length) {
      const messages = localStorage.getItem('messages')
      const listData = localStorage.getItem('listData')
      if(messages && listData) {
        setMessages(JSON.parse(messages))
        setListDataState(JSON.parse(listData))
        localStorage.removeItem('messages')
        localStorage.removeItem('listData')
      }
    }
  }, [messages, listDataState])
  return <div className="flex min-h-screen">
    <div className="left w-[260px]">
      <ConvasitionList listData={listDataState} id={id?.[0]}></ConvasitionList>
    </div>
    <div className="right flex-1">
      <ConvasitionBox id={id?.[0]} messages={messages} setMessages={setMessages} onSendNewMessage={sendNewMessage}></ConvasitionBox>
    </div>
  </div>
}