import { useState, useEffect, useRef } from 'react'
import { fetchConditionsList } from '../../utils/api'
import { Check, Plus, X } from 'lucide-react'

/**
 * Props:
 *   selectedIds      – array of predefined condition IDs currently selected
 *   customList       – array of custom condition strings currently saved
 *   onIdsChange      – (ids: string[]) => void
 *   onCustomChange   – (customs: string[]) => void
 */
export default function ConditionSelector({ selectedIds, customList, onIdsChange, onCustomChange }) {
  const [conditions, setConditions] = useState([])
  const [customInput, setCustomInput] = useState('')
  const [activeCategory, setActiveCategory] = useState('All')
  const didLoad = useRef(false)

  useEffect(() => {
    if (didLoad.current) return
    didLoad.current = true
    fetchConditionsList().then(setConditions).catch(console.error)
  }, [])

  const categories = ['All', ...new Set(conditions.map((c) => c.category))]

  const filtered = activeCategory === 'All'
    ? conditions
    : conditions.filter((c) => c.category === activeCategory)

  const toggle = (id) => {
    const next = selectedIds.includes(id)
      ? selectedIds.filter((s) => s !== id)
      : [...selectedIds, id]
    onIdsChange(next)
  }

  const addCustom = () => {
    const trimmed = customInput.trim()
    if (!trimmed || customList.includes(trimmed)) return
    onCustomChange([...customList, trimmed])
    setCustomInput('')
  }

  const removeCustom = (item) => {
    onCustomChange(customList.filter((c) => c !== item))
  }

  return (
    <div className="flex flex-col gap-4">
      {/* Category tabs */}
      <div className="flex flex-wrap gap-1.5">
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            onClick={() => setActiveCategory(cat)}
            className={`text-xs px-3 py-1 rounded-full transition-all ${
              activeCategory === cat
                ? 'bg-teal-600 text-white'
                : 'bg-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Conditions grid */}
      <div className="grid grid-cols-2 gap-2 max-h-52 overflow-y-auto pr-1">
        {filtered.map((cond) => {
          const isSelected = selectedIds.includes(cond.id)
          return (
            <button
              key={cond.id}
              type="button"
              onClick={() => toggle(cond.id)}
              className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs text-left transition-all border ${
                isSelected
                  ? 'bg-teal-600/20 border-teal-500/50 text-teal-300'
                  : 'bg-slate-800/60 border-slate-700/40 text-slate-400 hover:border-slate-500'
              }`}
            >
              <div className={`w-4 h-4 rounded flex items-center justify-center flex-shrink-0 border ${
                isSelected ? 'bg-teal-600 border-teal-600' : 'border-slate-600'
              }`}>
                {isSelected && <Check size={10} className="text-white" />}
              </div>
              {cond.label}
            </button>
          )
        })}
      </div>

      {/* Custom entry */}
      <div>
        <p className="text-xs text-slate-500 mb-2">Other (not listed above)</p>
        <div className="flex gap-2">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addCustom())}
            placeholder="Type condition name..."
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600"
          />
          <button
            type="button"
            onClick={addCustom}
            className="px-3 py-2 rounded-xl bg-teal-600 hover:bg-teal-500 text-white transition-all"
          >
            <Plus size={15} />
          </button>
        </div>
        {customList.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-2">
            {customList.map((item) => (
              <span
                key={item}
                className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full bg-violet-500/20 border border-violet-500/30 text-violet-300"
              >
                {item}
                <button type="button" onClick={() => removeCustom(item)}>
                  <X size={10} />
                </button>
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
