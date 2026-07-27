import api from './api'
import type { CourseRecord } from './courses'

export interface ChatMessageRecord {
  id: number
  role: string
  content: string
  created_at: string
  citations?: Array<{ document_name: string; page_number?: number; chunk_index: number; excerpt: string; relevance_score?: number }>
}

export interface ChatSessionRecord {
  id: number
  title: string
  course_id?: number
  course?: CourseRecord
  created_at: string
  updated_at: string
  messages: ChatMessageRecord[]
}

export async function fetchSessions() {
  const response = await api.get<ChatSessionRecord[]>('/ai/sessions')
  return response.data
}

export async function fetchSession(sessionId: number) {
  const response = await api.get<ChatSessionRecord>(`/ai/sessions/${sessionId}`)
  return response.data
}
