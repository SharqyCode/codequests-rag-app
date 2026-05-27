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
    <div className="
  flex items-center gap-3
  bg-zinc-900
  border border-zinc-800
  rounded-2xl
  p-2
">
      <input
        type="text"
        className="
  flex-1
  bg-transparent
  outline-none
  text-zinc-100
  placeholder:text-zinc-500
  px-2
"
        placeholder="Ask something..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
      />

      <button
        onClick={handleSubmit}
        disabled={disabled}
        className="
  bg-zinc-100
  text-zinc-900
  px-4 py-2
  rounded-xl
  hover:bg-white
  disabled:opacity-50
"
      >
        Send
      </button>
    </div>
  )
}