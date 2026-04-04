export function formatTime(date) {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

export function formatCategory(category) {
  if (!category || category === 'unknown') return null
  return category.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}

export const CATEGORY_COLORS = {
  symptoms: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
  medications: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  conditions: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
  anatomy: 'bg-pink-500/20 text-pink-300 border-pink-500/30',
  procedures: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
  nutrition: 'bg-green-500/20 text-green-300 border-green-500/30',
  mental_health: 'bg-violet-500/20 text-violet-300 border-violet-500/30',
  public_health: 'bg-teal-500/20 text-teal-300 border-teal-500/30',
  emergency: 'bg-red-500/20 text-red-300 border-red-500/30',
  non_medical: 'bg-slate-500/20 text-slate-300 border-slate-500/30',
  unknown: 'bg-slate-500/20 text-slate-400 border-slate-500/30',
}
