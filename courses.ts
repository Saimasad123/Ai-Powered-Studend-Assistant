import api from './api'

export interface CourseCreatePayload {
  course_name: string
  course_code?: string
  description?: string
}

export interface CourseRecord {
  id: number
  user_id: number
  course_name: string
  course_code?: string
  description?: string
  created_at: string
  updated_at: string
}

export async function fetchCourses() {
  const response = await api.get<CourseRecord[]>('/courses')
  return response.data
}

export async function createCourse(payload: CourseCreatePayload) {
  const response = await api.post<CourseRecord>('/courses', payload)
  return response.data
}
