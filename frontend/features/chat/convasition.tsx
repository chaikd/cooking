"use client"
import ConvasitionBox from "@/features/chat/convasition-box"
import ConvasitionList from "@/features/chat/convasition-list"
import { ConvasitionListItemType, sendMessage } from "@/services/api/session"
import { useState } from "react"

export default ({id, listData}: {
  id: string,
  listData: ConvasitionListItemType[]
}) => {
  const [listDataState, setListDataState] = useState<ConvasitionListItemType[]>(listData || [])
  const [localListData, setLocalListData] = useState<ConvasitionListItemType[]>([])
  const sendNewMessage = (
    messageInfo: any
  ) => {
    const newListData: ConvasitionListItemType[] = [{
      id: messageInfo.conversationId,
      title: messageInfo.message,
      conversationId: messageInfo.conversationId
    }]
    setLocalListData(newListData)
  }
  return <div className="flex h-screen">
    <div className="left w-[260px]">
      <ConvasitionList listData={listDataState} setListDataState={setListDataState} localListData={localListData} id={id?.[0]}></ConvasitionList>
    </div>
    <div className="right flex-1">
      <ConvasitionBox id={id?.[0]} onSendNewMessage={sendNewMessage}></ConvasitionBox>
    </div>
  </div>
}