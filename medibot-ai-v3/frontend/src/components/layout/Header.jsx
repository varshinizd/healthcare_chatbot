import { Stethoscope, Shield, Activity } from 'lucide-react'

export default function Header({ sessionId, queryCount }) {
  return (
    <header className="flex-shrink-0 flex items-center justify-between px-6 py-4 border-b border-slate-800/60 bg-slate-900/50 backdrop-blur-sm">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-teal-600 flex items-center justify-center shadow-lg shadow-teal-900/40">
          <Stethoscope size={18} className="text-white" />
        </div>
        <div>
          <h1 className="font-display text-lg text-white leading-none">MediBot <span className="text-teal-400">AI</span></h1>
          <p className="text-xs text-slate-500 mt-0.5">Medical Information Assistant</p>
        </div>
      </div>
    </header>
  )
}
