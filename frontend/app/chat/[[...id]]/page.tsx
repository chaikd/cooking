import ChatBox from "../section/chat-box"
import SessionList from "../section/session-list"

export default () => {
  return <div className="flex min-h-screen">
    <div className="left w-[260px]">
      <SessionList></SessionList>
    </div>
    <div className="right flex-1">
      <ChatBox></ChatBox>
    </div>
  </div>
}