import { useContext } from "react"
import { ChatContext } from "components/chat/ChatProvider"

const useChat = () => useContext(ChatContext)

export default useChat
