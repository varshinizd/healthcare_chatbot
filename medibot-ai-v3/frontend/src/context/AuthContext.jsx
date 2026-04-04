import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { fetchMe } from '../utils/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('medibot_token')
    if (token) {
      fetchMe()
        .then(setUser)
        .catch(() => localStorage.removeItem('medibot_token'))
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const loginUser = useCallback((token, userData) => {
    localStorage.setItem('medibot_token', token)
    setUser(userData)
  }, [])

  const logoutUser = useCallback(() => {
    localStorage.removeItem('medibot_token')
    setUser(null)
  }, [])

  const refreshUser = useCallback(async () => {
    const updated = await fetchMe()
    setUser(updated)
    return updated
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading, loginUser, logoutUser, refreshUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
