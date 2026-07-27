import { useEffect, useState, type FormEvent } from 'react'
import { useNavigate, Link, useSearchParams } from 'react-router-dom'
import { logout } from '../lib/auth'
import { askAI, AIResponse } from '../lib/ai'
import api from '../lib/api'

const actionOptions = [
  { label: 'Chat', value: 'chat' },
  { label: 'Summarize', value: 'summarize' },
  { label: 'Generate MCQs', value: 'generate-mcqs' },
  { label: 'Generate Quiz', value: 'generate-quiz' },
  { label: 'Generate flashcards', value: 'generate-flashcards' },
  { label: 'Explain topic', value: 'explain' },
  { label: 'Exam plan', value: 'exam-plan' },
]

export function StudyPage() {
  const navigate = useNavigate()
  const [question, setQuestion] = useState('')
  const [courseId, setCourseId] = useState('')
  const [courses, setCourses] = useState<{ id: number; course_name: string }[]>([])
  const [sessionId, setSessionId] = useState('')
  const [action, setAction] = useState('chat')
  const [response, setResponse] = useState<AIResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [searchParams] = useSearchParams()

  useEffect(() => {
    api
      .get('/auth/me')
      .catch(() => {
        logout()
        navigate('/login')
      })

    api.get('/courses')
      .then((response) => setCourses(response.data))
      .catch(() => {})

    const querySession = searchParams.get('session_id')
    const queryCourse = searchParams.get('course_id')
    if (querySession) {
      setSessionId(querySession)
    }
    if (queryCourse) {
      setCourseId(queryCourse)
    }
  }, [])

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError('')
    setResponse(null)

    if (!question.trim()) {
      setError('Please enter a question or topic.')
      return
    }

    setLoading(true)

    try {
      const bodyWithSession = {
        question,
        course_id: courseId ? Number(courseId) : undefined,
        session_id: sessionId ? Number(sessionId) : undefined,
      }
      const result = await askAI(bodyWithSession, action)
      setResponse(result)
    } catch (err) {
      setError((err as any)?.response?.data?.detail || 'Unable to generate a response. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="navbar">
        <div>Study Assistant</div>
        <div>
          <Link className="nav-link" to="/dashboard">Dashboard</Link>
          <Link className="nav-link" to="/documents">Documents</Link>
          <button className="button" onClick={() => { logout(); navigate('/login') }}>Logout</button>
        </div>
      </div>
      <div className="container">
        <div className="card">
          <h1>Ask the AI tutor</h1>
          <p>Use your uploaded materials to generate grounded answers, summaries, flashcards, and study plans.</p>
          <form onSubmit={handleSubmit}>
            <label>
              Action
              <select className="input" value={action} onChange={(event) => setAction(event.target.value)}>
                {actionOptions.map((option) => (
                  <option key={option.value} value={option.value}>{option.label}</option>
                ))}
              </select>
            </label>
            {sessionId && (
              <p style={{ fontSize: 14, margin: '0 0 12px' }}><strong>Resuming session:</strong> {sessionId}</p>
            )}
            <label>
              Course (optional)
              <select className="input" value={courseId} onChange={(event) => setCourseId(event.target.value)}>
                <option value="">All documents</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>{course.course_name}</option>
                ))}
              </select>
            </label>
            <label>
              Question or prompt
              <textarea
                className="input"
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                rows={6}
                required
              />
            </label>
            {error && <p style={{ color: 'red' }}>{error}</p>}
            <button className="button" type="submit" disabled={loading}>{loading ? 'Generating…' : 'Generate'}</button>
          </form>
        </div>

        {response && (
          <div className="card" style={{ marginTop: 24 }}>
            <h2>Result</h2>
            <p style={{ whiteSpace: 'pre-wrap' }}>{response.answer}</p>
            {response.citations?.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <h3>Citations</h3>
                <ul>
                  {response.citations.map((citation, index) => (
                    <li key={index} style={{ marginBottom: 8 }}>
                      <strong>{citation.document_name}</strong>
                      {citation.page_number ? ` · Page ${citation.page_number}` : ''}
                      <div>{citation.excerpt}</div>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {response.source_chunks?.length > 0 && (
              <div style={{ marginTop: 16 }}>
                <h3>Source chunks</h3>
                <ul>
                  {response.source_chunks.map((chunk, index) => (
                    <li key={index} style={{ marginBottom: 12, whiteSpace: 'pre-wrap' }}><strong>{chunk.document_name}</strong>{chunk.page_number ? ` · ${chunk.source_type === 'pptx' ? 'Slide' : 'Page'} ${chunk.page_number}` : ''}<div>{chunk.content}</div></li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
