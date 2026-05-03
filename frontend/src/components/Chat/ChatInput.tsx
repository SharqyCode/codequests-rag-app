import { useState } from "react"

type Props = {
  onSend: (message: string) => void
  disabled?: boolean
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [input, setInput] = useState("")

  const handleSubmit = () => {
    if (!input.trim()) return
    onSend(input)
    setInput("")
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSubmit()
    }
  }

  return (
    <div className="flex gap-2">
      <input
        type="text"
        className="flex-1 border rounded px-3 py-2"
        placeholder="Ask something..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
      />

      <button
        onClick={handleSubmit}
        disabled={disabled}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        Send
      </button>
    </div>
  )
}