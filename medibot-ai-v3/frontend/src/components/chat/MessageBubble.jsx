import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { ThumbsUp, ThumbsDown, Copy, Check, Stethoscope, Zap, Database } from 'lucide-react'
import { formatTime, formatCategory, CATEGORY_COLORS } from '../../utils/formatters'
import { useChat } from '../../context/ChatContext'

function UserBubble({ message }) {
  return (
    <div className="flex justify-end message-enter">
      <div className="max-w-[75%]">
        <div className="bg-teal-600 text-white px-4 py-3 rounded-2xl rounded-br-sm shadow-md shadow-teal-900/30">
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
        </div>
        <p className="text-right text-xs text-slate-600 mt-1 pr-1">{formatTime(message.timestamp)}</p>
      </div>
    </div>
  )
}

function BotBubble({ message }) {
  const { handleFeedback } = useChat()
  const [copied, setCopied] = useState(false)
  const category = formatCategory(message.category)
  const categoryStyle = CATEGORY_COLORS[message.category] || CATEGORY_COLORS.unknown

  const isEmergency = message.isEmergency
  const isBlocked = message.blocked && !message.isEmergency

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    })
  }

  const bubbleClass = isEmergency
    ? 'bg-red-950/60 border-red-700/60 emergency-pulse'
    : isBlocked
    ? 'bg-amber-950/30 border-amber-700/30'
    : 'bg-slate-800/80 border-slate-700/40'

  return (
    <div className="flex items-end gap-3 message-enter">
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 shadow-md ${
        isEmergency ? 'bg-red-600' : 'bg-teal-600 shadow-teal-900/40'
      }`}>
        <Stethoscope size={14} className="text-white" />
      </div>

      <div className="max-w-[80%] flex flex-col gap-1.5">
        {/* Metadata badges */}
        {(category || message.ragUsed) && !isEmergency && (
          <div className="flex items-center gap-2 flex-wrap">
            {category && (
              <span className={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full border ${categoryStyle}`}>
                {category}
              </span>
            )}
            {message.ragUsed && (
              <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20">
                <Database size={9} />
                RAG Enhanced
              </span>
            )}
          </div>
        )}

        {/* Message bubble */}
        <div className={`px-4 py-3.5 rounded-2xl rounded-bl-sm border ${bubbleClass}`}>
          {isEmergency && (
            <div className="flex items-center gap-2 mb-2 pb-2 border-b border-red-700/40">
              <div className="w-5 h-5 rounded-full bg-red-500 flex items-center justify-center">
                <span className="text-white text-xs font-bold">!</span>
              </div>
              <span className="text-xs font-semibold text-red-400 uppercase tracking-wider">Emergency Alert</span>
            </div>
          )}
          <div className="prose-medical text-slate-200 text-sm">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
          </div>
        </div>

        {/* Actions row */}
        <div className="flex items-center justify-between px-1">
          <span className="text-xs text-slate-600">{formatTime(message.timestamp)}</span>

          {!isEmergency && message.messageId && (
            <div className="flex items-center gap-1">
              <button
                onClick={handleCopy}
                className="p-1.5 rounded-lg text-slate-600 hover:text-slate-400 hover:bg-slate-700/50 transition-all"
                title="Copy"
              >
                {copied ? <Check size={13} className="text-teal-400" /> : <Copy size={13} />}
              </button>
              <button
                onClick={() => handleFeedback(message.messageId, 1)}
                className={`p-1.5 rounded-lg transition-all ${
                  message.feedbackScore === 1
                    ? 'text-emerald-400 bg-emerald-500/10'
                    : 'text-slate-600 hover:text-emerald-400 hover:bg-emerald-500/10'
                }`}
                title="Helpful"
              >
                <ThumbsUp size={13} />
              </button>
              <button
                onClick={() => handleFeedback(message.messageId, -1)}
                className={`p-1.5 rounded-lg transition-all ${
                  message.feedbackScore === -1
                    ? 'text-red-400 bg-red-500/10'
                    : 'text-slate-600 hover:text-red-400 hover:bg-red-500/10'
                }`}
                title="Not helpful"
              >
                <ThumbsDown size={13} />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default function MessageBubble({ message }) {
  if (message.role === 'user') return <UserBubble message={message} />
  return <BotBubble message={message} />
}
