import type { Document } from "../../lib/api"
import DocumentItem from "./DocumentItem"

type Props = {
  documents: Document[]
  onSelect: (doc: Document) => void
}

export default function DocumentList({ documents, onSelect }: Props) {
  if (!documents.length) {
    return <div className="text-gray-500">No documents found</div>
  }

  return (
    <div className="space-y-2">
      {documents.map((doc) => (
        <DocumentItem
          key={doc.document_id}
          document={doc}
          onClick={() => onSelect(doc)}
          isSelected = {doc.isSelected}
        />
      ))}
    </div>
  )
}