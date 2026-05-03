import { useEffect, useRef } from "react"
import MessageItem from "./Message"
import type { Message } from "../../context/ChatContext"

type Props = {
  messages: Message[]
  loading: boolean
}

export default function MessageList({ messages, loading }: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null)

  // Auto-scroll when messages or loading changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages, loading])

  return (
    <div className="space-y-4">
      {messages.map((msg, index) => (
        <MessageItem key={index} message={msg} />
      ))}

      {loading && (
        <div className="text-left text-gray-500 italic animate-pulse">
          AI is thinking...
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}