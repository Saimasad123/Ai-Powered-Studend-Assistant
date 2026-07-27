import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { register } from '../lib/auth'

export function RegisterPage() {
  const navigate = useNavigate()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      await register({ name, email, password })
      navigate('/login')
    } catch (err) {
      setError('Registration failed. Please try again.')
    }
  }

  return (
    <div className="container">
      <div className="card" style={{ maxWidth: 420, margin: '0 auto' }}>
        <h1>Create account</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Full name
            <input className="input" type="text" value={name} onChange={(event) => setName(event.target.value)} required />
          </label>
          <label>
            Email
            <input className="input" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
          </label>
          <label>
            Password
            <input className="input" type="password" value={password} onChange={(event) => setPassword(event.target.value)} required />
          </label>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <button className="button" type="submit">Register</button>
        </form>
        <p>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  )
}
