import api from './api'

export interface AIRequest {
  question: string
  course_id?: number
  session_id?: number
}

export interface CitationData {
  document_name: string
  page_number?: number
  source_type?: string
  chunk_index: number
  excerpt: string
  relevance_score?: number | null
}

export interface SourceChunk extends CitationData {
  content: string
  chunk_id: number
  document_id: number
}

export interface AIResponse {
  answer: string
  citations: CitationData[]
  source_chunks: SourceChunk[]
  session_id?: number
}

export async function askAI(request: AIRequest, action: string = 'chat') {
  const response = await api.post(`/ai/${action}`, request)
  return response.data as AIResponse
}
