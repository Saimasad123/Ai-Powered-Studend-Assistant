import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../lib/api'
import { logout } from '../lib/auth'
import type { CourseRecord } from '../lib/courses'

interface DocumentRecord {
  id: number
  original_filename: string
  file_type: string
  processing_status: string
  created_at: string
}

export function DocumentsPage() {
  const navigate = useNavigate()
  const [documents, setDocuments] = useState<DocumentRecord[]>([])
  const [courses, setCourses] = useState<CourseRecord[]>([])
  const [selectedCourseId, setSelectedCourseId] = useState('')
  const [files, setFiles] = useState<FileList | null>(null)
  const [status, setStatus] = useState('')
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    api.get('/documents')
      .then((response) => setDocuments(response.data))
      .catch(() => {
        logout()
        navigate('/login')
      })

    api.get('/courses')
      .then((response) => setCourses(response.data))
      .catch(() => {})
  }, [])

  const refreshDocuments = async () => {
    setRefreshing(true)
    try {
      const response = await api.get('/documents')
      setDocuments(response.data)
    } finally {
      setRefreshing(false)
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!files?.length) {
      return
    }
    const formData = new FormData()
    for (const file of Array.from(files)) {
      formData.append('files', file)
    }
    try {
      if (selectedCourseId) {
        formData.append('course_id', selectedCourseId)
      }
      setStatus('Uploading…')
      const response = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setDocuments((prev) => [...prev, ...response.data])
      setStatus('Upload complete. Processing has started. Refresh to see the latest status.')
      await refreshDocuments()
    } catch (error) {
      setStatus('Upload failed. Please try again.')
    }
  }

  return (
    <div>
      <div className="navbar">
        <div>Documents</div>
        <div>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
          <button className="button" onClick={() => { logout(); navigate('/login') }}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="card">
          <h1>Upload materials</h1>
          <form onSubmit={handleSubmit}>
            <label>
              Course (optional)
              <select className="input" value={selectedCourseId} onChange={(event) => setSelectedCourseId(event.target.value)}>
                <option value="">All documents</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>{course.course_name}</option>
                ))}
              </select>
            </label>
            <input className="input" type="file" multiple onChange={(event) => setFiles(event.target.files)} />
            <button className="button" type="submit">Upload</button>
          </form>
          {status && <p>{status}</p>}
        </div>
        <div className="card">
          <h2>Your documents</h2>
          <button className="button" type="button" onClick={refreshDocuments} disabled={refreshing}>{refreshing ? 'Refreshing…' : 'Refresh status'}</button>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left', padding: '12px' }}>Filename</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Type</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Status</th>
                <th style={{ textAlign: 'left', padding: '12px' }}>Uploaded</th>
              </tr>
            </thead>
            <tbody>
              {documents.map((doc) => (
                <tr key={doc.id}>
                  <td style={{ padding: '12px' }}>{doc.original_filename}</td>
                  <td style={{ padding: '12px' }}>{doc.file_type}</td>
                  <td style={{ padding: '12px' }}>{doc.processing_status}</td>
                  <td style={{ padding: '12px' }}>{new Date(doc.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
