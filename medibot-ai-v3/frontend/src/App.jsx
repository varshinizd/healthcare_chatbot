import { useState, useEffect } from 'react'
import { AuthProvider, useAuth } from './context/AuthContext'
import { ChatProvider, useChat } from './context/ChatContext'
import Header from './components/layout/Header'
import Sidebar from './components/layout/Sidebar'
import DisclaimerBanner from './components/layout/DisclaimerBanner'
import AboutView from './components/layout/AboutView'
import ProfilePage from './components/layout/ProfilePage'
import ChatWindow from './components/chat/ChatWindow'
import InputBar from './components/chat/InputBar'
import EmergencyModal from './components/modals/EmergencyModal'
import HipaaModal from './components/modals/HipaaModal'
import LoginPage from './components/auth/LoginPage'
import SignupPage from './components/auth/SignupPage'

const HIPAA_KEY = 'medibot_hipaa_accepted'

function AuthGate({ children }) {
  const { user, loading } = useAuth()
  const [authView, setAuthView] = useState('login')

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-teal-600 animate-pulse" />
          <p className="text-slate-500 text-sm">Loading...</p>
        </div>
      </div>
    )
  }

  if (!user) {
    if (authView === 'signup') return <SignupPage onGoLogin={() => setAuthView('login')} />
    return <LoginPage onGoSignup={() => setAuthView('signup')} />
  }

  return children
}

function AppInner() {
  const [activeView, setActiveView] = useState('chat')
  const [showHipaa, setShowHipaa] = useState(false)
  const { isLoading, showEmergencyModal, setShowEmergencyModal, sessionId, queryCount, sendMessage } = useChat()
  const { user } = useAuth()

  useEffect(() => {
    const accepted = localStorage.getItem(HIPAA_KEY)
    if (!accepted) setShowHipaa(true)
  }, [])

  const handleHipaaAccept = () => {
    localStorage.setItem(HIPAA_KEY, '1')
    setShowHipaa(false)
  }

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      <div className="hidden lg:flex">
        <Sidebar activeView={activeView} onViewChange={setActiveView} />
      </div>

      <div className="flex flex-col flex-1 min-w-0">
        <Header sessionId={sessionId} queryCount={queryCount} />
        <DisclaimerBanner />

        {activeView === 'about' && <AboutView />}
        {activeView === 'profile' && <ProfilePage />}
        {activeView === 'chat' && (
          <>
            <ChatWindow onSend={sendMessage} />
            <InputBar onSend={sendMessage} isLoading={isLoading} />
          </>
        )}
      </div>

      {showHipaa && <HipaaModal onAccept={handleHipaaAccept} />}
      {showEmergencyModal && <EmergencyModal onClose={() => setShowEmergencyModal(false)} />}
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <AuthGate>
        <ChatProvider>
          <AppInner />
        </ChatProvider>
      </AuthGate>
    </AuthProvider>
  )
}
