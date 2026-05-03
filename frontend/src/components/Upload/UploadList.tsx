type Props = {
  uploadedIds: string[]
}

export default function UploadList({ uploadedIds }: Props) {
  if (!uploadedIds.length) return null

  return (
    <div className="mt-6">
      <h2 className="font-semibold mb-2">Uploaded Documents</h2>

      <ul className="list-disc ml-5 text-sm text-gray-700">
        {uploadedIds.map((id, index) => (
          <li key={index}>{id}</li>
        ))}
      </ul>
    </div>
  )
}