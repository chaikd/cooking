"use client"
import classNames from "classnames"
import { redirect } from "next/navigation"
import { useEffect, useState } from "react"

export interface ConvasitionListItemType {
    id: string,
    title: string
  }
export default ({id, listData}: {
  id: string,
  listData: ConvasitionListItemType[]
}) => {
  const [active, setActive] = useState('')
  useEffect(() => {
    if(active && id !== active) {
      redirect(`/chat/${active}`)
    }
  }, [active, id])
  useEffect(() => {
    if(!active && !id && listData?.length) {
      setActive(listData[listData.length - 1].id)
    } else if(id && !active && listData.some(v => id === v.id)) {
      setActive(id)
    }
  }, [listData])
  return <div className="h-full border-r-1 border-gray-300 p-2">
    {
      listData?.length && (listData.map(v => {
        return <span 
          key={v.id} 
          className={classNames(
            'w-full inline-block p-2 mb-2 rounded hover:bg-gray-300 cursor-pointer',
            {'bg-gray-100': active === v.id}
          )}
          onClick={() => setActive(v.id)}>
            {v.title}
          </span>
      })) || '暂无数据，在右侧发起聊天'
    }
  </div>
}