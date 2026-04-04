import { createContext, useContext, useState, useCallback } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { sendChatMessage, submitFeedback } from '../utils/api'

const ChatContext = createContext(null)

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [queryCount, setQueryCount] = useState(0)
  const [showEmergencyModal, setShowEmergencyModal] = useState(false)
  const [emergencyData, setEmergencyData] = useState(null)
  const [error, setError] = useState(null)

  const addMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, { id: uuidv4(), timestamp: Date.now(), ...msg }])
  }, [])

  const sendMessage = useCallback(async (text) => {
    if (!text.trim() || isLoading) return

    addMessage({ role: 'user', content: text })
    setIsLoading(true)
    setError(null)

    try {
      const data = await sendChatMessage({ message: text, sessionId })
      if (!sessionId && data.session_id) setSessionId(data.session_id)

      addMessage({
        role: 'assistant',
        content: data.reply,
        messageId: data.message_id,
        blocked: data.blocked,
        blockReason: data.block_reason,
        isEmergency: data.is_emergency,
        category: data.category,
        ragUsed: data.rag_used,
        latencyMs: data.latency_ms,
        isClarifyingQuestion: data.is_clarifying_question,
      })
      setQueryCount((c) => c + 1)

      if (data.is_emergency) {
        setEmergencyData({ message: text })
        setShowEmergencyModal(true)
      }
    } catch (err) {
      setError(err.message)
      addMessage({
        role: 'assistant',
        content: '⚠️ Unable to reach the MediBot server. Please ensure the backend is running on port 8000.',
        isError: true,
      })
    } finally {
      setIsLoading(false)
    }
  }, [isLoading, sessionId, addMessage])

  const clearChat = useCallback(() => {
    setMessages([])
    setSessionId(null)
    setQueryCount(0)
    setError(null)
  }, [])

  const handleFeedback = useCallback(async (messageId, score) => {
    if (!sessionId || !messageId) return
    await submitFeedback({ sessionId, messageId, score })
    setMessages((prev) =>
      prev.map((m) => (m.messageId === messageId ? { ...m, feedbackScore: score } : m))
    )
  }, [sessionId])

  return (
    <ChatContext.Provider value={{
      messages, isLoading, sessionId, queryCount, error,
      showEmergencyModal, setShowEmergencyModal, emergencyData,
      sendMessage, clearChat, handleFeedback,
    }}>
      {children}
    </ChatContext.Provider>
  )
}

export function useChat() {
  const ctx = useContext(ChatContext)
  if (!ctx) throw new Error('useChat must be used within ChatProvider')
  return ctx
}
