import type { Document } from "../../lib/api"

type Props = {
  document: Document
  onClick: () => void
  isSelected?: boolean
}

export default function DocumentItem({ document, onClick, isSelected }: Props) {
  return (
    <div
      onClick={onClick}
      className={`border p-3 rounded cursor-pointer ${
      isSelected ? "bg-blue-100" : "hover:bg-gray-100"
      }`}
    >
      <div className="font-medium">{document.source}</div>
      <div className="text-xs text-gray-500">
        ID: {document.document_id}
      </div>
    </div>
  )
}