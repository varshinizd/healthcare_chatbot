import { useEffect, useRef } from 'react'
import { Stethoscope, HeartPulse } from 'lucide-react'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'
import QuickPrompts from './QuickPrompts'
import { useChat } from '../../context/ChatContext'

function WelcomeState({ onQuickPrompt }) {
  return (
    <div className="flex flex-col items-center justify-center h-full gap-8 px-4">
      <div className="flex flex-col items-center gap-4 text-center">
        <div className="relative">
          <div className="w-20 h-20 rounded-3xl bg-teal-600 flex items-center justify-center shadow-2xl shadow-teal-900/50">
            <Stethoscope size={36} className="text-white" />
          </div>
          <div className="absolute -top-1 -right-1 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center shadow-md">
            <HeartPulse size={12} className="text-white" />
          </div>
        </div>
        <div>
          <h2 className="font-display text-3xl text-white mb-2">
            Hello, I'm <span className="text-teal-400">MediBot</span>
          </h2>
          <p className="text-slate-400 text-sm max-w-sm leading-relaxed">
            Your intelligent medical information assistant. I can help with symptoms,
            conditions, medications, and general health questions.
          </p>
        </div>
      </div>
      <QuickPrompts onSelect={onQuickPrompt} />
    </div>
  )
}

export default function ChatWindow({ onSend }) {
  const { messages, isLoading } = useChat()
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  if (messages.length === 0 && !isLoading) {
    return (
      <div className="flex-1 overflow-y-auto chat-bg">
        <WelcomeState onQuickPrompt={onSend} />
      </div>
    )
  }

  return (
    <div className="flex-1 overflow-y-auto chat-bg px-4 py-6">
      <div className="max-w-3xl mx-auto flex flex-col gap-5">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
