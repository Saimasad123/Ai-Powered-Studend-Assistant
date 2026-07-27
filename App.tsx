import { Routes, Route, Navigate } from 'react-router-dom'
import { DashboardPage } from './pages/DashboardPage'
import { LoginPage } from './pages/LoginPage'
import { RegisterPage } from './pages/RegisterPage'
import { DocumentsPage } from './pages/DocumentsPage'
import { StudyPage } from './pages/StudyPage'
import { CoursesPage } from './pages/CoursesPage'
import { HistoryPage } from './pages/HistoryPage'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
      <Route path="/documents" element={<DocumentsPage />} />
      <Route path="/study" element={<StudyPage />} />
      <Route path="/courses" element={<CoursesPage />} />
      <Route path="/history" element={<HistoryPage />} />
    </Routes>
  )
}
