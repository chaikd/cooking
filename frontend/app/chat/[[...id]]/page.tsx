import ConvasitionBox from "@/features/chat/convasition-box"
import ConvasitionList from "@/features/chat/convasition-list"

export default async ({params}: {
  params: Promise<{id: string}>
}) => {
  const {id} = await params
  return <div className="flex min-h-screen">
    <div className="left w-[260px]">
      <ConvasitionList></ConvasitionList>
    </div>
    <div className="right flex-1">
      <ConvasitionBox id={id}></ConvasitionBox>
    </div>
  </div>
}