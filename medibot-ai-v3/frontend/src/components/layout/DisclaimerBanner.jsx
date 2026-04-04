import { AlertTriangle, X } from 'lucide-react'
import { useState } from 'react'

export default function DisclaimerBanner() {
  const [dismissed, setDismissed] = useState(false)
  if (dismissed) return null

  return (
    <div className="flex-shrink-0 flex items-center gap-3 px-4 py-2.5 bg-amber-500/10 border-b border-amber-500/20">
      <AlertTriangle size={14} className="text-amber-400 flex-shrink-0" />
      <p className="text-xs text-amber-300/80 flex-1">
        <strong className="text-amber-300">Not medical advice.</strong>{' '}
        MediBot AI provides general health information only. Always consult a qualified healthcare professional.
        <strong className="text-amber-300"> For emergencies, call 108 immediately.</strong>
      </p>
      <button
        onClick={() => setDismissed(true)}
        className="flex-shrink-0 p-0.5 rounded hover:bg-amber-500/20 transition-colors"
        aria-label="Dismiss"
      >
        <X size={12} className="text-amber-400" />
      </button>
    </div>
  )
}
