import { useState } from 'react'
import { Stethoscope, Eye, EyeOff, Loader2, ChevronRight, ChevronLeft } from 'lucide-react'
import { signup } from '../../utils/api'
import { useAuth } from '../../context/AuthContext'
import ConditionSelector from '../shared/ConditionSelector'

const GENDER_OPTIONS = ['Male', 'Female', 'Other', 'Prefer not to say']
const BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-', "Don't know"]
const SMOKING_OPTIONS = ['Never', 'Former smoker', 'Current smoker']
const ALCOHOL_OPTIONS = ['Never', 'Occasionally', 'Regularly']

function SelectInput({ label, value, onChange, options, placeholder = 'Select...' }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}</label>
      <select
        value={value || ''}
        onChange={(e) => onChange(e.target.value || null)}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 outline-none focus:border-teal-600 transition-colors"
      >
        <option value="">{placeholder}</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )
}

function TextInput({ label, value, onChange, type = 'text', placeholder, unit }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}{unit && <span className="text-slate-600 ml-1">({unit})</span>}</label>
      <input
        type={type}
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value === '' ? null : (type === 'number' ? Number(e.target.value) : e.target.value))}
        placeholder={placeholder}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600 transition-colors"
      />
    </div>
  )
}

function TextareaInput({ label, value, onChange, placeholder }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}</label>
      <textarea
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value || null)}
        placeholder={placeholder}
        rows={2}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600 transition-colors resize-none"
      />
    </div>
  )
}

const STEPS = ['Account', 'Health Info', 'Conditions']

export default function SignupPage({ onGoLogin }) {
  const { loginUser } = useAuth()
  const [step, setStep] = useState(0)
  const [showPass, setShowPass] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [account, setAccount] = useState({ email: '', username: '', password: '', full_name: '' })
  const [health, setHealth] = useState({
    age: null, gender: null, blood_group: null,
    height_cm: null, weight_kg: null,
    allergies: null, current_medications: null,
    smoking_status: null, alcohol_status: null,
  })
  const [selectedIds, setSelectedIds] = useState([])
  const [customList, setCustomList] = useState([])

  const setHealthField = (key) => (val) => setHealth((h) => ({ ...h, [key]: val }))

  const validateStep0 = () => {
    if (!account.email || !account.username || !account.password) {
      setError('Please fill in all required fields.')
      return false
    }
    if (account.password.length < 6) {
      setError('Password must be at least 6 characters.')
      return false
    }
    return true
  }

  const handleNext = () => {
    setError('')
    if (step === 0 && !validateStep0()) return
    setStep((s) => s + 1)
  }

  const handleSubmit = async () => {
    setError('')
    setLoading(true)
    try {
      const data = await signup({
        ...account,
        ...health,
        condition_ids: selectedIds,
        custom_conditions: customList,
      })
      loginUser(data.access_token, data.user)
    } catch (err) {
      setError(err.message)
      setStep(0)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 rounded-3xl bg-teal-600 flex items-center justify-center mx-auto mb-4 shadow-2xl shadow-teal-900/50">
            <Stethoscope size={28} className="text-white" />
          </div>
          <h1 className="font-display text-3xl text-white">Create account</h1>
          <p className="text-slate-400 text-sm mt-1">Your personal medical assistant</p>
        </div>

        {/* Step bar */}
        <div className="flex items-center mb-6 px-2">
          {STEPS.map((label, i) => (
            <div key={i} className="flex items-center flex-1 last:flex-none">
              <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold transition-all ${
                i <= step ? 'bg-teal-600 text-white' : 'bg-slate-800 text-slate-500'
              }`}>{i + 1}</div>
              <span className={`text-xs ml-1.5 ${i === step ? 'text-teal-400' : 'text-slate-600'}`}>{label}</span>
              {i < STEPS.length - 1 && (
                <div className={`flex-1 h-px mx-2 ${step > i ? 'bg-teal-600' : 'bg-slate-800'}`} />
              )}
            </div>
          ))}
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 flex flex-col gap-5">
          {error && (
            <div className="px-4 py-3 rounded-xl bg-red-950/50 border border-red-700/40 text-sm text-red-300">
              {error}
            </div>
          )}

          {/* Step 0 — Account */}
          {step === 0 && (
            <>
              <TextInput label="Full Name" value={account.full_name}
                onChange={(v) => setAccount((a) => ({ ...a, full_name: v || '' }))} placeholder="John Doe" />
              <TextInput label="Username *" value={account.username}
                onChange={(v) => setAccount((a) => ({ ...a, username: v || '' }))} placeholder="johndoe" />
              <TextInput label="Email *" value={account.email} type="email"
                onChange={(v) => setAccount((a) => ({ ...a, email: v || '' }))} placeholder="you@example.com" />
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-medium text-slate-400">Password *</label>
                <div className="relative">
                  <input
                    type={showPass ? 'text' : 'password'}
                    value={account.password}
                    onChange={(e) => setAccount((a) => ({ ...a, password: e.target.value }))}
                    placeholder="Min. 6 characters"
                    className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600 pr-10"
                  />
                  <button type="button" onClick={() => setShowPass(!showPass)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300">
                    {showPass ? <EyeOff size={15} /> : <Eye size={15} />}
                  </button>
                </div>
              </div>
            </>
          )}

          {/* Step 1 — Health Info */}
          {step === 1 && (
            <>
              <p className="text-xs text-slate-500">This helps MediBot personalise responses. All fields optional.</p>
              <div className="grid grid-cols-2 gap-4">
                <TextInput label="Age" value={health.age} onChange={setHealthField('age')} type="number" placeholder="25" />
                <SelectInput label="Gender" value={health.gender} onChange={setHealthField('gender')} options={GENDER_OPTIONS} />
                <SelectInput label="Blood Group" value={health.blood_group} onChange={setHealthField('blood_group')} options={BLOOD_GROUPS} />
                <div />
                <TextInput label="Height" value={health.height_cm} onChange={setHealthField('height_cm')} type="number" placeholder="170" unit="cm" />
                <TextInput label="Weight" value={health.weight_kg} onChange={setHealthField('weight_kg')} type="number" placeholder="65" unit="kg" />
              </div>
              <SelectInput label="Smoking Status" value={health.smoking_status} onChange={setHealthField('smoking_status')} options={SMOKING_OPTIONS} />
              <SelectInput label="Alcohol Consumption" value={health.alcohol_status} onChange={setHealthField('alcohol_status')} options={ALCOHOL_OPTIONS} />
              <TextareaInput label="Known Allergies" value={health.allergies} onChange={setHealthField('allergies')} placeholder="e.g. Penicillin, Peanuts..." />
              <TextareaInput label="Current Medications" value={health.current_medications} onChange={setHealthField('current_medications')} placeholder="e.g. Metformin 500mg..." />
            </>
          )}

          {/* Step 2 — Conditions */}
          {step === 2 && (
            <>
              <div>
                <h3 className="text-sm font-semibold text-slate-200 mb-1">Diagnosed Conditions</h3>
                <p className="text-xs text-slate-500 mb-4">
                  Select any conditions you've been diagnosed with. You can skip and update later.
                </p>
                <ConditionSelector
                  selectedIds={selectedIds}
                  customList={customList}
                  onIdsChange={setSelectedIds}
                  onCustomChange={setCustomList}
                />
              </div>
            </>
          )}

          {/* Navigation */}
          <div className="flex gap-3 pt-1">
            {step > 0 && (
              <button type="button" onClick={() => setStep((s) => s - 1)}
                className="flex-1 py-3 rounded-2xl border border-slate-700 text-slate-400 hover:text-white hover:border-slate-500 text-sm transition-all flex items-center justify-center gap-2">
                <ChevronLeft size={15} /> Back
              </button>
            )}
            {step < STEPS.length - 1 ? (
              <button type="button" onClick={handleNext}
                className="flex-1 py-3 rounded-2xl bg-teal-600 hover:bg-teal-500 text-white font-semibold text-sm transition-all flex items-center justify-center gap-2">
                Next <ChevronRight size={15} />
              </button>
            ) : (
              <button type="button" onClick={handleSubmit} disabled={loading}
                className="flex-1 py-3 rounded-2xl bg-teal-600 hover:bg-teal-500 disabled:opacity-50 text-white font-semibold text-sm transition-all flex items-center justify-center gap-2">
                {loading && <Loader2 size={15} className="animate-spin" />}
                {loading ? 'Creating...' : 'Create Account'}
              </button>
            )}
          </div>

          <p className="text-center text-sm text-slate-500">
            Already have an account?{' '}
            <button onClick={onGoLogin} className="text-teal-400 hover:text-teal-300 font-medium">Sign in</button>
          </p>
        </div>
      </div>
    </div>
  )
}
