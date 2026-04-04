import { Stethoscope, MessageSquare, Info, Trash2, User, Shield } from 'lucide-react'
import { useChat } from '../../context/ChatContext'
import { useAuth } from '../../context/AuthContext'

export default function Sidebar({ activeView, onViewChange }) {
  const { sessionId, queryCount, clearChat } = useChat()
  const { user } = useAuth()
  const shortId = sessionId ? sessionId.slice(-8) : '--------'
  const conditionCount = user?.conditions?.length || 0

  const navItems = [
    { id: 'chat', icon: MessageSquare, label: 'Chat' },
    { id: 'profile', icon: User, label: 'Profile' },
    { id: 'about', icon: Info, label: 'About' },
  ]

  return (
    <aside className="w-64 flex-shrink-0 bg-slate-950 border-r border-slate-800/60 flex flex-col">
      <div className="px-5 py-6 border-b border-slate-800/60">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center">
            <Stethoscope size={18} className="text-white" />
          </div>
          <div>
            <h1 className="font-display text-base text-white leading-none">
              MediBot <span className="text-teal-400">AI</span>
            </h1>
            <span className="text-xs text-slate-600">v2.0.0</span>
          </div>
        </div>
      </div>

      {/* User greeting */}
      {user && (
        <div className="px-4 pt-4 pb-2">
          <div className="bg-teal-950/30 border border-teal-800/30 rounded-xl px-3 py-2.5">
            <p className="text-xs text-slate-400">Signed in as</p>
            <p className="text-sm font-medium text-teal-300">{user.full_name || user.username}</p>
            {conditionCount > 0 && (
              <div className="flex items-center gap-1 mt-1">
                <Shield size={10} className="text-teal-500" />
                <span className="text-xs text-slate-500">{conditionCount} condition{conditionCount > 1 ? 's' : ''} tracked</span>
              </div>
            )}
          </div>
        </div>
      )}

      <nav className="flex-1 px-3 py-3 flex flex-col gap-1">
        {navItems.map(({ id, icon: Icon, label }) => (
          <button
            key={id}
            onClick={() => onViewChange(id)}
            className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
              activeView === id
                ? 'bg-teal-600/20 text-teal-300 border border-teal-600/30'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
            }`}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </nav>

      <div className="px-4 py-4 border-t border-slate-800/60 flex flex-col gap-3">
        <button
          onClick={clearChat}
          className="flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs text-slate-500 hover:text-red-400 hover:bg-red-950/30 border border-transparent hover:border-red-900/40 transition-all"
        >
          <Trash2 size={12} />
          Clear Chat
        </button>
      </div>

      <div className="px-4 py-3 border-t border-slate-800/40">
        <p className="text-xs text-slate-700 text-center">Powered by Gemini AI</p>
      </div>
    </aside>
  )
}
