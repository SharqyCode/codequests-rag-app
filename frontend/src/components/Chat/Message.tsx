import type { Message } from "../../pages/ChatPage"
import SourceList from "./SourceList"

type Props = {
  message: Message
}

export default function MessageItem({ message }: Props) {
  const isUser = message.role === "user"

  return (
    <div className={isUser ? "text-right" : "text-left"}>
      <div
        className={`inline-block px-4 py-2 rounded max-w-[70%] ${
          isUser
            ? "bg-blue-500 text-white"
            : "bg-gray-200 text-black"
        }`}
      >
        {message.text}
      </div>

      {!isUser && message.sources && (
        <SourceList sources={message.sources} />
      )}
    </div>
  )
}