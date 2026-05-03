import { createContext, useContext, useEffect, useState } from "react"

// ==============================
// Types
// ==============================

export type Source = {
  source: string
  document_id: string
}

export type Message = {
  role: "user" | "ai"
  text: string
  sources?: Source[]
}

// ==============================
// Context Type
// ==============================

type ChatContextType = {
  messages: Message[]
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>
  clearMessages: () => void
}

// ==============================
// Create Context
// ==============================

const ChatContext = createContext<ChatContextType | null>(null)

// ==============================
// Provider
// ==============================

export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([])

  // Load from localStorage
  useEffect(() => {
    try {
      const stored = localStorage.getItem("chat_messages")
      if (stored) {
        setMessages(JSON.parse(stored))
      }
    } catch {
      console.warn("Failed to parse stored chat messages")
    }
  }, [])

  // Save to localStorage
  useEffect(() => {
    localStorage.setItem("chat_messages", JSON.stringify(messages))
  }, [messages])

  // ✅ Clear function
  const clearMessages = () => {
    setMessages([]) // 1. clear state
    localStorage.removeItem("chat_messages") // 2. clear storage
  }

  return (
    <ChatContext.Provider
      value={{ messages, setMessages, clearMessages }}
    >
      {children}
    </ChatContext.Provider>
  )
}

// ==============================
// Hook
// ==============================

export function useChat() {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error("useChat must be used within ChatProvider")
  }
  return context
}