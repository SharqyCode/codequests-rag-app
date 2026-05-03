import type { Source } from "../../pages/ChatPage"
import { useNavigate } from "react-router-dom"

type Props = {
  sources: Source[]
}

export default function SourceList({ sources }: Props) {
  const navigate = useNavigate()

  if (!sources.length) return null

  const handleClick = (documentId: string) => {
    navigate(`/docs?docId=${documentId}`)
  }

  return (
    <div className="mt-2 text-sm text-gray-600">
      <div className="font-semibold">Sources:</div>
      <ul className="list-disc ml-5">
        {sources.map((s, index) => (
          <li
            key={index}
            onClick={() => handleClick(s.document_id)}
            className="cursor-pointer text-blue-600 hover:underline"
          >
            {s.source}
          </li>
        ))}
      </ul>
    </div>
  )
}