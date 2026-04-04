import { Stethoscope, ShieldCheck, Eye, AlertTriangle } from 'lucide-react'

const ITEMS = [
  {
    icon: ShieldCheck,
    iconColor: 'text-teal-400',
    bg: 'bg-teal-500/10',
    title: 'Informational Only',
    desc: 'MediBot provides general health information, not medical advice or diagnosis.',
  },
  {
    icon: Eye,
    iconColor: 'text-blue-400',
    bg: 'bg-blue-500/10',
    title: 'Data & Privacy',
    desc: 'Conversations are processed to generate responses. Avoid sharing personal identifiers.',
  },
  {
    icon: AlertTriangle,
    iconColor: 'text-amber-400',
    bg: 'bg-amber-500/10',
    title: 'Emergency Situations',
    desc: 'For life-threatening emergencies, call 108 (or local emergency number) — do not rely on this chatbot.',
  },
]

export default function HipaaModal({ onAccept }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700/60 rounded-3xl shadow-2xl w-full max-w-md animate-slide-up overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-br from-teal-900/60 to-slate-900 border-b border-slate-800/60 px-6 pt-8 pb-6 text-center">
          <div className="w-16 h-16 rounded-3xl bg-teal-600 flex items-center justify-center mx-auto mb-4 shadow-xl shadow-teal-900/50">
            <Stethoscope size={28} className="text-white" />
          </div>
          <h2 className="font-display text-2xl text-white mb-1">Before You Begin</h2>
          <p className="text-sm text-slate-400">Please read these important notes</p>
        </div>

        {/* Items */}
        <div className="p-6 flex flex-col gap-4">
          {ITEMS.map(({ icon: Icon, iconColor, bg, title, desc }) => (
            <div key={title} className="flex gap-3">
              <div className={`w-9 h-9 rounded-xl ${bg} flex items-center justify-center flex-shrink-0`}>
                <Icon size={16} className={iconColor} />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-200">{title}</p>
                <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">{desc}</p>
              </div>
            </div>
          ))}

          <div className="mt-2 p-3 rounded-xl bg-slate-800/50 border border-slate-700/40">
            <p className="text-xs text-slate-500 text-center leading-relaxed">
              By continuing, you acknowledge that MediBot AI is a{' '}
              <strong className="text-slate-400">computer science project</strong> for educational purposes
              and does not replace professional medical care.
            </p>
          </div>

          <button
            onClick={onAccept}
            className="w-full py-3.5 rounded-2xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-sm transition-all shadow-lg shadow-teal-900/40 mt-1"
          >
            I Understand — Continue
          </button>
        </div>
      </div>
    </div>
  )
}
