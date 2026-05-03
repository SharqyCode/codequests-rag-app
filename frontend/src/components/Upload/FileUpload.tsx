type Props = {
  files: File[]
  setFiles: React.Dispatch<React.SetStateAction<File[]>>
}

export default function FileUpload({ files, setFiles }: Props) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files) return

    const selected = Array.from(e.target.files)

    // append instead of replace
    setFiles((prev) => [...prev, ...selected])
  }

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="border p-4 rounded">
      <input
        type="file"
        multiple
        onChange={handleChange}
        className="mb-4"
      />

      {files.length > 0 && (
        <ul className="space-y-2">
          {files.map((file, index) => (
            <li
              key={index}
              className="flex justify-between items-center border px-3 py-2 rounded"
            >
              <span className="truncate">{file.name}</span>

              <button
                onClick={() => removeFile(index)}
                className="text-red-500 text-sm"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}