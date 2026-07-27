import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { logout } from '../lib/auth'
import { fetchCourses, createCourse, type CourseRecord } from '../lib/courses'
import api from '../lib/api'

export function CoursesPage() {
  const navigate = useNavigate()
  const [courses, setCourses] = useState<CourseRecord[]>([])
  const [name, setName] = useState('')
  const [code, setCode] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/auth/me')
      .catch(() => {
        logout()
        navigate('/login')
      })

    loadCourses()
  }, [])

  const loadCourses = async () => {
    try {
      const result = await fetchCourses()
      setCourses(result)
    } catch (err) {
      setError('Unable to load courses.')
    }
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!name.trim()) {
      setError('Course name is required.')
      return
    }

    setLoading(true)
    setError('')

    try {
      const newCourse = await createCourse({
        course_name: name,
        course_code: code || undefined,
        description: description || undefined,
      })
      setCourses((prev) => [newCourse, ...prev])
      setName('')
      setCode('')
      setDescription('')
    } catch (err) {
      setError('Unable to create course. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="navbar">
        <div>Courses</div>
        <div>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
          <Link className="nav-link" to="/documents">Documents</Link>
          <Link className="nav-link" to="/study">Study</Link>
          <button className="button" onClick={() => { logout(); navigate('/login') }}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="card">
          <h1>Create a course</h1>
          <form onSubmit={handleSubmit}>
            <label>
              Name
              <input className="input" value={name} onChange={(event) => setName(event.target.value)} required />
            </label>
            <label>
              Code
              <input className="input" value={code} onChange={(event) => setCode(event.target.value)} />
            </label>
            <label>
              Description
              <textarea className="input" value={description} onChange={(event) => setDescription(event.target.value)} rows={3} />
            </label>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button className="button" type="submit" disabled={loading}>{loading ? 'Creating…' : 'Create course'}</button>
          </form>
        </div>
        <div className="card" style={{ marginTop: 24 }}>
          <h2>Your courses</h2>
          {courses.length === 0 ? (
            <p>No courses yet. Create one to organize your documents and study sessions.</p>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '12px' }}>Name</th>
                  <th style={{ textAlign: 'left', padding: '12px' }}>Code</th>
                  <th style={{ textAlign: 'left', padding: '12px' }}>Description</th>
                </tr>
              </thead>
              <tbody>
                {courses.map((course) => (
                  <tr key={course.id}>
                    <td style={{ padding: '12px' }}>{course.course_name}</td>
                    <td style={{ padding: '12px' }}>{course.course_code || '—'}</td>
                    <td style={{ padding: '12px' }}>{course.description || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  )
}
