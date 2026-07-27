import api from './api'

export interface LoginPayload {
  email: string
  password: string
}

export interface RegisterPayload {
  name: string
  email: string
  password: string
}

export async function login(payload: LoginPayload) {
  const response = await api.post('/auth/login', payload)
  localStorage.setItem('access_token', response.data.access_token)
  return response.data
}

export async function register(payload: RegisterPayload) {
  const response = await api.post('/auth/register', payload)
  return response.data
}

export function logout() {
  localStorage.removeItem('access_token')
}
