import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login } from '../lib/auth'

export function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      await login({ email, password })
      navigate('/dashboard')
    } catch (err) {
      setError('Invalid email or password')
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 420, margin: '0 auto' }}>
        <h1>Login</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Email
            <input className="input" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label>
            Password
            <input className="input" type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
          </label>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <button className="button" type="submit">Sign in</button>
        </form>
        <p>
          New to the platform? <Link to="/register">Create an account</Link>
        </p>
      </div>
    </div>
  )
}
