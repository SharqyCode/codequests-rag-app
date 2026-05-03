import type { Document } from "../../lib/api"

type Props = {
  document: Document | null
}

export default function DocumentViewer({ document }: Props) {
  if (!document) {
    return (
      <div className="text-gray-500">
        Select a document to view details
      </div>
    )
  }

  return (
    <div>
      <h2 className="text-xl font-bold mb-2">
        {document.source}
      </h2>

      <div className="text-sm text-gray-500 mb-4">
        Document ID: {document.document_id}
      </div>

      <div className="text-sm text-gray-500 mb-4">
        Content : {document.content}
      </div>

      {/* Placeholder for future chunk view */}
      <div className="text-gray-700">
        Document details loaded successfully.
      </div>
    </div>
  )
}