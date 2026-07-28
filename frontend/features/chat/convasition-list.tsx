"use client"
import { ConvasitionListItemType } from "@/services/api/session"
import { Button } from "antd"
import classNames from "classnames"
import { redirect } from "next/navigation"
import { useEffect, useState } from "react"


export default ({id, listData, localListData, setListDataState}: {
  id: string,
  listData: ConvasitionListItemType[],
  localListData: ConvasitionListItemType[],
  setListDataState: (datalist: ConvasitionListItemType[]) => void
}) => {
  const [active, setActive] = useState('')
  useEffect(() => {
    let localData: any = localStorage.getItem('localListData')
    if(!id && localListData?.length) {
      localStorage.setItem('localListData', JSON.stringify(localListData))
      redirect(`/chat/${localListData[0].conversationId}`)
    } else if(id && localData) {
      localStorage.removeItem('localListData')
      localData = JSON.parse(localData) as ConvasitionListItemType[]
      setListDataState([...localData, ...listData])
    }
  }, [localListData])
  useEffect(() => {
    if((id && !active)) {
      setActive(id)
    } else if(id && listData.every(v => v.conversationId !== id)) {
      redirect('/chat')
    } else if(active && active !== id) {
      redirect(`/chat/${active}`)
    }
  }, [active, id])
  return <div className="h-full border-r-1 border-gray-300 p-2">
    <Button className="w-full" href="/chat">开启新对话</Button>
    {
      listData?.length && (listData.map(v => {
        return <span 
          key={v.id} 
          className={classNames(
            'w-full inline-block p-2 mb-2 rounded hover:bg-gray-100 cursor-pointer',
            {'bg-gray-300': active === v.conversationId}
          )}
          onClick={() => {
            setActive(v.conversationId)
          }}>
            {v.title}
          </span>
      })) || '暂无数据，在右侧发起聊天'
    }
  </div>
}