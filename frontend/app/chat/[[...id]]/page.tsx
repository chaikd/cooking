import Convasition from "@/features/chat/convasition"
import { getSessionList } from "@/services/api/session"

export default async ({params}: {
  params: Promise<{id: string}>
}) => {
  const {id} = await params
  const listData = await getSessionList()

  return <Convasition id={id} listData={listData}/>
}