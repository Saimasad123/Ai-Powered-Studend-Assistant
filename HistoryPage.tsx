import { useEffect, useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { logout } from '../lib/auth'
import api from '../lib/api'
import { fetchSessions, type ChatSessionRecord } from '../lib/history'

export function HistoryPage() {
  const navigate = useNavigate()
  const [sessions, setSessions] = useState<ChatSessionRecord[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/auth/me').catch(() => {
      logout()
      navigate('/login')
    })

    fetchSessions()
      .then((data) => setSessions(data))
      .catch(() => setError('Unable to load chat history.'))
  }, [])

  return (
    <div>
      <div className="navbar">
        <div>Chat History</div>
        <div>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
          <Link className="nav-link" to="/study">Study</Link>
          <button className="button" onClick={() => { logout(); navigate('/login') }}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="card">
          <h1>Past study sessions</h1>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {sessions.length === 0 ? (
            <p>No study sessions yet. Start one from the Study page.</p>
          ) : (
            <ul>
              {sessions.map((session) => (
                <li key={session.id} style={{ marginBottom: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong>{session.title}</strong>
                    <Link className="button" to={`/study?session_id=${session.id}${session.course_id ? `&course_id=${session.course_id}` : ''}`}>Resume</Link>
                  </div>
                  <div style={{ color: '#666', marginTop: 4 }}>
                    {session.course?.course_name ? `Course: ${session.course.course_name}` : 'General study session'}
                  </div>
                  <div style={{ fontSize: 13, marginTop: 4 }}>{new Date(session.updated_at).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}
