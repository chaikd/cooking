import { getSessionList } from "@/services/api/session"

export default async () => {
  const listData = await getSessionList()
  return <div className="h-full border-r-1 border-gray-300 p-2 box-content">
    {
      listData?.length && (listData.map(v => {
        return <span key={v.id} className="w-full inline-block p-2 mb-2 rounded hover:bg-gray-100 cursor-pointer">{v.name}</span>
      })) || '暂无数据，在右侧发起聊天'
    }
  </div>
}