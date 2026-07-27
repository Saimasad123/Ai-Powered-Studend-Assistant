import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import api from '../lib/api'
import { logout } from '../lib/auth'

export function DashboardPage() {
  const navigate = useNavigate()
  const [profile, setProfile] = useState<{ name: string; email: string } | null>(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api
      .get('/auth/me')
      .then((response) => setProfile(response.data))
      .catch(() => {
        logout()
        navigate('/login')
      })
  }, [])

  return (
    <div>
      <div className="navbar">
        <div>{profile ? `Welcome, ${profile.name}` : 'Student Assistant'}</div>
        <div>
          <Link className="nav-link" to="/courses">Courses</Link>
          <Link className="nav-link" to="/study">Study</Link>
          <Link className="nav-link" to="/documents">Documents</Link>
          <Link className="nav-link" to="/history">History</Link>
          <button className="button" onClick={() => { logout(); navigate('/login') }}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="header">
          <div>
            <h1>Dashboard</h1>
            <p>Upload academic materials, ask questions, and study smarter.</p>
          </div>
        </div>
        {error && <p style={{ color: 'red' }}>{error}</p>}
        <div className="grid" style={{ gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))' }}>
          <div className="card">
            <h2>Manage courses</h2>
            <p>Create course sections to organize documents and study sessions.</p>
            <Link className="button" to="/courses">Manage courses</Link>
          </div>
          <div className="card">
            <h2>Review history</h2>
            <p>Open previous AI sessions and continue study conversations.</p>
            <Link className="button" to="/history">View history</Link>
          </div>
          <div className="card">
            <h2>Upload documents</h2>
            <p>Bring in lecture notes, PDFs and slides for AI-backed learning.</p>
            <Link className="button" to="/documents">Manage documents</Link>
          </div>
        </div>
      </div>
    </div>
  )
}
