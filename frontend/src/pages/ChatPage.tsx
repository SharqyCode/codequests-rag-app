import { useState } from "react"
import ChatInput from "../components/Chat/ChatInput"
import MessageList from "../components/Chat/MessageList"
import { queryAI, streamAIResponse } from "../lib/api"
import { useChat, type Message } from "../context/ChatContext"

export default function ChatPage() {
  const { messages, setMessages, clearMessages } = useChat()
  const [loading, setLoading] = useState(false)

  // --------- Get and display complete response---------
  // const handleSend = async (input: string) => {
  //   if (!input.trim() || loading) return

  //   const userMessage: Message = {
  //     role: "user",
  //     text: input,
  //   }

  //   setMessages((prev) => [...prev, userMessage])
  //   setLoading(true)

  //   try {
  //     const response = await queryAI({ query: input })

  //     const aiMessage: Message = {
  //       role: "ai",
  //       text: response.answer,
  //       sources: response.sources,
  //     }

  //     setMessages((prev) => [...prev, aiMessage])
  //   } catch (error: any) {
  //     setMessages((prev) => [
  //       ...prev,
  //       {
  //         role: "ai",
  //         text:
  //           error?.message || "Something went wrong. Please try again.",
  //       },
  //     ])
  //   } finally {
  //     setLoading(false)
  //   }
  // }

  // --------- Get and display streamed response---------
  const handleSend = async (input: string) => {
    if (!input.trim() || loading) return

    const userMessage: Message = {
      role: "user",
      text: input,
    }

    const aiMessage: Message = {
      role: "ai",
      text: "",
      sources: [],
    }

    setMessages((prev) => [...prev, userMessage, aiMessage])

    setLoading(true)

    try {
      await streamAIResponse(
        { query: input },
        (chunk) => {
          setMessages((prev) => {
            const updated = [...prev]

            const last = updated[updated.length - 1]

            updated[updated.length - 1] = {
              ...last,
              text: last.text + chunk,
            }

            return updated
          })
        }
      )
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text:
            error?.message || "Something went wrong.",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-full ">
      <div className="flex-1 overflow-y-auto mb-4">
        <MessageList messages={messages} loading={loading} />
      </div>

      <ChatInput onSend={handleSend} disabled={loading} />
      <button onClick={clearMessages} className="my-2 text-sm text-red-500">
        Clear Chat
      </button>
    </div>
  )
}