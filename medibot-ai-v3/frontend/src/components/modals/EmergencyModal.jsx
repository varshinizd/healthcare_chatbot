import { Phone, X, AlertTriangle } from 'lucide-react'

const EMERGENCY_NUMBERS = [
  { country: 'USA / Canada', number: '911' },
  { country: 'UK', number: '999' },
  { country: 'EU', number: '112' },
  { country: 'Australia', number: '000' },
  { country: 'India', number: '102 / 112' },
]

export default function EmergencyModal({ onClose }) {
  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm animate-fade-in"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="bg-slate-900 border border-red-700/60 rounded-3xl shadow-2xl shadow-red-950/50 w-full max-w-md emergency-pulse animate-slide-up overflow-hidden">
        {/* Header */}
        <div className="bg-red-950/60 border-b border-red-800/40 px-6 py-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-red-600 flex items-center justify-center shadow-lg">
              <AlertTriangle size={20} className="text-white" />
            </div>
            <div>
              <h2 className="font-display text-xl text-white">Medical Emergency</h2>
              <p className="text-xs text-red-300 mt-0.5">Immediate action required</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-xl text-slate-400 hover:text-white hover:bg-slate-700/60 transition-all"
          >
            <X size={18} />
          </button>
        </div>

        {/* Body */}
        <div className="p-6 flex flex-col gap-5">
          <p className="text-slate-200 text-sm leading-relaxed">
            Your message may describe a <strong className="text-red-400">medical emergency</strong>.
            Please do not wait for an AI response — call emergency services immediately.
          </p>

          {/* Emergency numbers */}
          <div className="bg-red-950/30 border border-red-800/30 rounded-2xl p-4">
            <p className="text-xs font-semibold text-red-400 uppercase tracking-wider mb-3">
              Emergency Numbers
            </p>
            <div className="grid grid-cols-2 gap-2">
              {EMERGENCY_NUMBERS.map(({ country, number }) => (
                <div key={country} className="flex items-center gap-2">
                  <Phone size={11} className="text-red-400 flex-shrink-0" />
                  <div>
                    <span className="text-xs text-slate-400">{country}: </span>
                    <span className="text-sm font-bold text-white">{number}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800/40 border border-slate-700/30 rounded-xl p-3">
            <p className="text-xs text-slate-400 leading-relaxed">
              After calling emergency services, you may return here for supporting information.
              MediBot AI is <strong className="text-slate-300">not</strong> a substitute for emergency care.
            </p>
          </div>

          <button
            onClick={onClose}
            className="w-full py-3 rounded-2xl bg-red-600 hover:bg-red-500 text-white font-semibold text-sm transition-all shadow-lg shadow-red-950/40"
          >
            I understand — Emergency services called
          </button>
        </div>
      </div>
    </div>
  )
}
