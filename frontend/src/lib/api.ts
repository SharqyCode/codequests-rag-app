// ==============================
// Base Config
// ==============================

const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

// ==============================
// Types
// ==============================

// ---- AI ----
export type Source = {
  source: string
  document_id: string
}

export type QueryResponse = {
  answer: string
  sources: Source[]
  confidence: number
}

export type QueryRequest = {
  query: string
  document_id?: string
}

// ---- Documents ----
export type Document = {
  document_id: string
  source: string
  content?: string
  isSelected?: boolean
}

// ---- Generic API Error ----
export type APIError = {
  detail?: string
  message?: string
}

// ==============================
// Generic Request Helper
// ==============================

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${BASE_URL}${endpoint}`

  const response = await fetch(url, {
    credentials: "include", // safe default
    ...options,
    headers: {
      ...(options.headers || {}),
    },
  })

  let data: any = null

  try {
    data = await response.json()
  } catch {
    // ignore JSON parse errors (e.g. empty response)
  }

  if (!response.ok) {
    const errorMessage =
      data?.detail ||
      data?.message ||
      `Request failed with status ${response.status}`

    throw new Error(errorMessage)
  }

  return data as T
}

// ==============================
// API Methods
// ==============================

// ---- AI Query ----
export async function queryAI(
  payload: QueryRequest
): Promise<QueryResponse> {
  return request<QueryResponse>("/api/ai/query", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
}

// ---- Upload Files ----
export async function uploadFiles(files: File[]): Promise<string[]> {
  const formData = new FormData()

  files.forEach((file) => {
    formData.append("files", file)
  })

  return request<string[]>("/api/ingest/files", {
    method: "POST",
    body: formData,
  })
}

// ---- Get All Documents ----
export async function getDocuments(): Promise<Document[]> {
  return request<Document[]>("/api/docs", {
    method: "GET",
  })
}

// ---- Get Document By ID ----
export async function getDocumentById(
  id: string
): Promise<Document> {
  return request<Document>(`/api/docs/${id}`, {
    method: "GET",
  })
}

