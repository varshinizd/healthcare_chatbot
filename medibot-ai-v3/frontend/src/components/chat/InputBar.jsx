import { useState, useRef } from 'react'
import { Send, AlertTriangle, Loader2 } from 'lucide-react'
import { useEmergencyDetect } from '../../hooks/useEmergencyDetect'

export default function InputBar({ onSend, isLoading }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)
  const emergencyWarning = useEmergencyDetect(value)

  const handleSubmit = () => {
    const trimmed = value.trim()
    if (!trimmed || isLoading) return
    onSend(trimmed)
    setValue('')
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  const handleInput = (e) => {
    setValue(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 160) + 'px'
  }

  return (
    <div className="flex-shrink-0 p-4 border-t border-slate-800/60 bg-slate-900/70 backdrop-blur-sm">
      {/* Emergency warning banner */}
      {emergencyWarning && (
        <div className="flex items-center gap-2 mb-3 px-3 py-2 rounded-xl bg-red-950/50 border border-red-700/40 animate-fade-in">
          <AlertTriangle size={14} className="text-red-400 flex-shrink-0" />
          <p className="text-xs text-red-300">
            <strong>Possible emergency detected.</strong> If this is a medical emergency, call{' '}
            <strong>911</strong> immediately — do not wait for a chatbot response.
          </p>
        </div>
      )}

      <div className={`flex items-end gap-3 rounded-2xl border transition-all duration-200 px-4 py-3 ${
        emergencyWarning
          ? 'bg-red-950/20 border-red-700/40'
          : 'bg-slate-800/60 border-slate-700/50 focus-within:border-teal-600/60 focus-within:bg-slate-800'
      }`}>
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleInput}
          onKeyDown={handleKeyDown}
          placeholder="Ask a medical question… (Shift+Enter for new line)"
          rows={1}
          className="flex-1 bg-transparent text-sm text-slate-200 placeholder-slate-500 resize-none outline-none leading-relaxed"
          style={{ minHeight: '24px', maxHeight: '160px' }}
          disabled={isLoading}
        />
        <button
          onClick={handleSubmit}
          disabled={!value.trim() || isLoading}
          className="flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center transition-all duration-150
                     disabled:opacity-30 disabled:cursor-not-allowed
                     bg-teal-600 hover:bg-teal-500 shadow-md shadow-teal-900/40"
          aria-label="Send message"
        >
          {isLoading ? (
            <Loader2 size={15} className="text-white animate-spin" />
          ) : (
            <Send size={14} className="text-white" />
          )}
        </button>
      </div>
      <p className="text-center text-xs text-slate-700 mt-2">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  )
}
