import { Shield, Zap, Database, Brain, AlertTriangle, BookOpen } from 'lucide-react'

const FEATURES = [
  { icon: Brain, title: 'Gemini 2.5 Flash', desc: 'Powered by Google\'s latest multimodal LLM for accurate medical information.' },
  { icon: Database, title: 'Profile Injection', desc: 'User health profile dynamically injected into every Gemini prompt for personalized, context-aware responses.' },
  { icon: Shield, title: 'Multi-Layer Guardrails', desc: '7-layer safety pipeline: emergency detection, input sanitization, classifier, RAG, generation, validation, and audit.' },
  { icon: AlertTriangle, title: 'Emergency Detection', desc: 'Real-time regex-based emergency detection covering 40+ patterns across 6 categories.' },
  { icon: Zap, title: 'Domain Restriction', desc: 'AI classifier blocks non-medical queries with confidence scoring and fail-open design.' },
  { icon: BookOpen, title: 'Academic Project', desc: 'Final year CS project demonstrating NLP, system design, and healthcare AI ethics.' },
]

const STACK = [
  { label: 'Backend', items: ['Python 3.11', 'FastAPI', 'Google Gemini AI', 'ChromaDB', 'SQLAlchemy'] },
  { label: 'Frontend', items: ['React 18', 'Vite', 'Tailwind CSS', 'react-markdown'] },
]

export default function AboutView() {
  return (
    <div className="flex-1 overflow-y-auto chat-bg px-6 py-8">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h2 className="font-display text-3xl text-white mb-2">About MediBot AI</h2>
          <p className="text-slate-400 leading-relaxed">
            An intelligent, domain-restricted medical conversational agent built as a final-year
            computer science project. Demonstrates advanced NLP, RAG, multi-layer AI safety,
            and healthcare AI ethics.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8">
          {FEATURES.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="glass-card rounded-2xl p-4">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-8 h-8 rounded-xl bg-teal-600/20 border border-teal-600/30 flex items-center justify-center">
                  <Icon size={15} className="text-teal-400" />
                </div>
                <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
              </div>
              <p className="text-xs text-slate-500 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>

        <div className="glass-card rounded-2xl p-5 mb-6">
          <h3 className="text-sm font-semibold text-slate-200 mb-4">Technology Stack</h3>
          <div className="grid grid-cols-2 gap-4">
            {STACK.map(({ label, items }) => (
              <div key={label}>
                <p className="text-xs text-teal-400 font-semibold uppercase tracking-wider mb-2">{label}</p>
                <ul className="flex flex-col gap-1">
                  {items.map((item) => (
                    <li key={item} className="text-xs text-slate-400 flex items-center gap-1.5">
                      <span className="w-1 h-1 rounded-full bg-teal-600" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        <div className="glass-card rounded-2xl p-4 border-amber-500/20 bg-amber-950/10">
          <p className="text-xs text-amber-300/80 leading-relaxed">
            <strong className="text-amber-300">⚠️ Important:</strong> MediBot AI is an educational
            project and does not provide medical advice. Always consult a qualified healthcare
            professional for diagnosis and treatment.
          </p>
        </div>
      </div>
    </div>
  )
}
