import { useState } from "react"
import FileUpload from "../components/Upload/FileUpload"
import UploadList from "../components/Upload/UploadList"
import { uploadFiles } from "../lib/api"

export default function UploadPage() {
  const [files, setFiles] = useState<File[]>([])
  const [uploading, setUploading] = useState(false)
  const [uploadedIds, setUploadedIds] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async () => {
    if (!files.length || uploading) return

    setUploading(true)
    setError(null)

    try {
      const result = await uploadFiles(files)
      setUploadedIds(result)

      // clear files after success
      setFiles([])
    } catch (err: any) {
      setError(err.message || "Upload failed")
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="
  bg-zinc-900
  border border-zinc-800
  rounded-2xl
  p-6
  shadow-sm
">
      <h1 className="text-2xl font-bold mb-4">Upload Documents</h1>

      <FileUpload files={files} setFiles={setFiles} />

      <button
        onClick={handleUpload}
        disabled={!files.length || uploading}
        className="mt-4 bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {uploading ? "Uploading..." : "Upload Files"}
      </button>

      {error && (
        <div className="mt-4 text-red-500">
          {error}
        </div>
      )}

      <UploadList uploadedIds={uploadedIds} />
    </div>
  )
}