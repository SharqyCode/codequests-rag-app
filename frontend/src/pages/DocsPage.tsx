import { useEffect, useState } from "react"
import { getDocuments, getDocumentById, type Document } from "../lib/api"
import DocumentList from "../components/Docs/DocumentList"
import DocumentViewer from "../components/Docs/DocumentViewer"
import { useSearchParams } from "react-router-dom"

export default function DocsPage() {
  const [documents, setDocuments] = useState<Document[]>([])
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [searchParams] = useSearchParams()
  const docIdFromURL = searchParams.get("docId")
  
  // Fetch all documents on load
  useEffect(() => {
    const fetchDocs = async () => {
      setLoading(true)
      setError(null)

      try {
        const {documents: data} = await getDocuments()
        setDocuments(data)

        // 🔥 Auto-select if docId exists
        if (docIdFromURL) {
          const found = data.find(
            (doc) => 
              {
                console.log(doc.document_id , docIdFromURL,  doc.document_id === docIdFromURL)
                return doc.document_id === docIdFromURL
              }
          )


          if (found) {
            handleSelect(found)
          }
        }
      } catch (err: any) {
        setError(err.message || "Failed to load documents")
      } finally {
        setLoading(false)
      }
    }

  fetchDocs()
}, [docIdFromURL])

  // Handle selecting a document
  const handleSelect = async (doc: Document) => {
    setLoading(true)

    searchParams.set("docId", doc.document_id)
    doc.isSelected = (doc.document_id === docIdFromURL)

    try {
      // If your backend returns more details, use this
      const fullDoc = await getDocumentById(doc.document_id)
      setSelectedDoc(fullDoc)
    } catch (err: any) {
      setError(err.message || "Failed to load document")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex">
      {/* Left: Document List */}
      <div className="w-1/3 border-r p-4 overflow-y-auto">
        <h2 className="text-xl font-bold mb-4">Documents</h2>

        {loading && <div className="text-gray-500">Loading...</div>}
        {error && <div className="text-red-500">{error}</div>}

        <DocumentList
          documents={documents}
          onSelect={handleSelect}
        />
      </div>

      {/* Right: Viewer */}
      <div className="flex-1 p-4 overflow-y-auto">
        <DocumentViewer document={selectedDoc} />
      </div>
    </div>
  )
}