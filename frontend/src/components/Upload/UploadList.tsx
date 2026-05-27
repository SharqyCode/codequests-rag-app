type Props = {
  uploadedIds: string[]
}

export default function UploadList({ uploadedIds }: Props) {
  if (!uploadedIds.length) return null

  return (
    <div className="mt-6">
      <h2 className="text-3xl font-semibold tracking-tight">Uploaded Documents</h2>

      <ul className="list-disc ml-5 text-sm text-gray-700">
        {uploadedIds.map((id, index) => (
          <li className="
            text-xs
            px-2 py-1
            rounded-lg
            bg-zinc-800
            hover:bg-zinc-700
            cursor-pointer
            inline-flex
            items-center
          " key={index}>{id}</li>
        ))}
      </ul>
    </div>
  )
}