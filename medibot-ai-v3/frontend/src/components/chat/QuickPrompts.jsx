import { QUICK_PROMPTS } from '../../constants/quickPrompts'

export default function QuickPrompts({ onSelect }) {
  return (
    <div className="px-4 pb-4">
      <p className="text-xs text-slate-600 mb-3 text-center">Suggested questions</p>
      <div className="flex flex-wrap gap-2 justify-center">
        {QUICK_PROMPTS.map((prompt) => (
          <button
            key={prompt.label}
            onClick={() => onSelect(prompt.text)}
            className="text-xs px-3 py-1.5 rounded-full bg-slate-800/60 border border-slate-700/50 text-slate-400
                       hover:border-teal-600/50 hover:text-teal-300 hover:bg-teal-950/30
                       transition-all duration-150 whitespace-nowrap"
          >
            {prompt.label}
          </button>
        ))}
      </div>
    </div>
  )
}
