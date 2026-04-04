import { useState, useEffect } from 'react'
import { User, Edit3, Save, X, Loader2, LogOut, Shield, Heart } from 'lucide-react'
import { updateProfile, fetchConditionsList } from '../../utils/api'
import { useAuth } from '../../context/AuthContext'
import ConditionSelector from '../shared/ConditionSelector'

const GENDER_OPTIONS = ['Male', 'Female', 'Other', 'Prefer not to say']
const BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-', "Don't know"]
const SMOKING_OPTIONS = ['Never', 'Former smoker', 'Current smoker']
const ALCOHOL_OPTIONS = ['Never', 'Occasionally', 'Regularly']

function SelectField({ label, value, onChange, options, placeholder = 'Select...' }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}</label>
      <select
        value={value || ''}
        onChange={(e) => onChange(e.target.value || null)}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 outline-none focus:border-teal-600 transition-colors"
      >
        <option value="">{placeholder}</option>
        {options.map((o) => <option key={o} value={o}>{o}</option>)}
      </select>
    </div>
  )
}

function InputField({ label, value, onChange, type = 'text', placeholder, unit }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}{unit && <span className="text-slate-600 ml-1">({unit})</span>}</label>
      <input
        type={type}
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value === '' ? null : (type === 'number' ? Number(e.target.value) : e.target.value))}
        placeholder={placeholder}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600 transition-colors"
      />
    </div>
  )
}

function TextareaField({ label, value, onChange, placeholder }) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-medium text-slate-400">{label}</label>
      <textarea
        value={value ?? ''}
        onChange={(e) => onChange(e.target.value || null)}
        placeholder={placeholder}
        rows={2}
        className="bg-slate-800 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-600 outline-none focus:border-teal-600 transition-colors resize-none"
      />
    </div>
  )
}

function bmiLabel(h, w) {
  if (!h || !w) return null
  const bmi = w / ((h / 100) ** 2)
  let cat = bmi < 18.5 ? 'Underweight' : bmi < 25 ? 'Normal' : bmi < 30 ? 'Overweight' : 'Obese'
  return `${bmi.toFixed(1)} — ${cat}`
}

// Build condition IDs from label names (reverse map)
function buildSelectedIds(userConditions, allConditions) {
  const labelToId = {}
  allConditions.forEach((c) => { labelToId[c.label] = c.id })
  return userConditions
    .filter((c) => !c.is_custom)
    .map((c) => labelToId[c.condition_name])
    .filter(Boolean)
}

export default function ProfilePage() {
  const { user, logoutUser, refreshUser } = useAuth()
  const [editing, setEditing] = useState(false)
  const [allConditions, setAllConditions] = useState([])

  // Form state
  const [form, setForm] = useState({
    full_name: user?.full_name || '',
    age: user?.age || null,
    gender: user?.gender || null,
    blood_group: user?.blood_group || null,
    height_cm: user?.height_cm || null,
    weight_kg: user?.weight_kg || null,
    allergies: user?.allergies || null,
    current_medications: user?.current_medications || null,
    smoking_status: user?.smoking_status || null,
    alcohol_status: user?.alcohol_status || null,
  })
  const [selectedIds, setSelectedIds] = useState([])
  const [customList, setCustomList] = useState([])
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState('')

  // Load conditions list to do reverse mapping
  useEffect(() => {
    fetchConditionsList().then(setAllConditions).catch(console.error)
  }, [])

  // When editing starts, pre-populate condition selection from user data
  useEffect(() => {
    if (editing && allConditions.length > 0 && user?.conditions) {
      setSelectedIds(buildSelectedIds(user.conditions, allConditions))
      setCustomList(user.conditions.filter((c) => c.is_custom).map((c) => c.condition_name))
    }
  }, [editing, allConditions])

  const setField = (key) => (val) => setForm((f) => ({ ...f, [key]: val }))

  const handleSave = async () => {
    setLoading(true)
    setError('')
    try {
      await updateProfile({
        ...form,
        condition_ids: selectedIds,
        custom_conditions: customList,
      })
      await refreshUser()
      setEditing(false)
      setSuccess(true)
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleCancelEdit = () => {
    setEditing(false)
    setError('')
    // Reset form to current user values
    setForm({
      full_name: user?.full_name || '',
      age: user?.age || null,
      gender: user?.gender || null,
      blood_group: user?.blood_group || null,
      height_cm: user?.height_cm || null,
      weight_kg: user?.weight_kg || null,
      allergies: user?.allergies || null,
      current_medications: user?.current_medications || null,
      smoking_status: user?.smoking_status || null,
      alcohol_status: user?.alcohol_status || null,
    })
  }

  const conditions = user?.conditions || []
  const bmi = bmiLabel(user?.height_cm, user?.weight_kg)

  return (
    <div className="flex-1 overflow-y-auto chat-bg px-6 py-8">
      <div className="max-w-2xl mx-auto flex flex-col gap-6">

        {/* Header */}
        <div className="glass-card rounded-3xl p-6 flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-teal-600 flex items-center justify-center shadow-lg shadow-teal-900/40">
            <User size={28} className="text-white" />
          </div>
          <div className="flex-1">
            <h2 className="font-display text-xl text-white">{user?.full_name || user?.username}</h2>
            <p className="text-sm text-slate-400">{user?.email}</p>
            <p className="text-xs text-slate-600 mt-0.5">@{user?.username}</p>
          </div>
          <button
            onClick={logoutUser}
            className="flex items-center gap-2 px-3 py-2 rounded-xl text-sm text-slate-500 hover:text-red-400 hover:bg-red-950/20 border border-transparent hover:border-red-900/40 transition-all"
          >
            <LogOut size={14} /> Logout
          </button>
        </div>

        {success && (
          <div className="px-4 py-3 rounded-xl bg-emerald-950/50 border border-emerald-700/40 text-sm text-emerald-300">
            ✓ Profile updated successfully!
          </div>
        )}
        {error && (
          <div className="px-4 py-3 rounded-xl bg-red-950/50 border border-red-700/40 text-sm text-red-300">
            {error}
          </div>
        )}

        {/* Edit / Save toolbar */}
        <div className="flex justify-end gap-2">
          {!editing ? (
            <button
              onClick={() => setEditing(true)}
              className="flex items-center gap-2 text-sm text-teal-400 hover:text-teal-300 px-4 py-2 rounded-xl hover:bg-teal-950/30 border border-teal-800/30 transition-all"
            >
              <Edit3 size={14} /> Edit Profile
            </button>
          ) : (
            <>
              <button onClick={handleCancelEdit} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-300 px-3 py-2 rounded-xl transition-all">
                <X size={14} /> Cancel
              </button>
              <button
                onClick={handleSave}
                disabled={loading}
                className="flex items-center gap-2 text-sm text-white bg-teal-600 hover:bg-teal-500 px-4 py-2 rounded-xl transition-all disabled:opacity-50"
              >
                {loading ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
                Save Changes
              </button>
            </>
          )}
        </div>

        {/* ── BASIC INFO ── */}
        <div className="glass-card rounded-3xl p-6 flex flex-col gap-5">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <User size={15} className="text-teal-400" /> Basic Information
          </h3>
          {editing ? (
            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2">
                <InputField label="Full Name" value={form.full_name} onChange={setField('full_name')} placeholder="John Doe" />
              </div>
              <InputField label="Age" value={form.age} onChange={setField('age')} type="number" placeholder="25" />
              <SelectField label="Gender" value={form.gender} onChange={setField('gender')} options={GENDER_OPTIONS} />
              <SelectField label="Blood Group" value={form.blood_group} onChange={setField('blood_group')} options={BLOOD_GROUPS} />
              <div /> {/* spacer */}
              <InputField label="Height" value={form.height_cm} onChange={setField('height_cm')} type="number" placeholder="170" unit="cm" />
              <InputField label="Weight" value={form.weight_kg} onChange={setField('weight_kg')} type="number" placeholder="65" unit="kg" />
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-y-3 gap-x-6">
              {[
                ['Full Name', user?.full_name],
                ['Age', user?.age ? `${user.age} years` : null],
                ['Gender', user?.gender],
                ['Blood Group', user?.blood_group],
                ['Height', user?.height_cm ? `${user.height_cm} cm` : null],
                ['Weight', user?.weight_kg ? `${user.weight_kg} kg` : null],
                ['BMI', bmi],
              ].map(([label, val]) => (
                <div key={label}>
                  <p className="text-xs text-slate-600">{label}</p>
                  <p className="text-sm text-slate-300">{val || <span className="text-slate-600 italic">Not set</span>}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ── LIFESTYLE ── */}
        <div className="glass-card rounded-3xl p-6 flex flex-col gap-5">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Heart size={15} className="text-rose-400" /> Lifestyle
          </h3>
          {editing ? (
            <div className="grid grid-cols-2 gap-4">
              <SelectField label="Smoking Status" value={form.smoking_status} onChange={setField('smoking_status')} options={SMOKING_OPTIONS} />
              <SelectField label="Alcohol Consumption" value={form.alcohol_status} onChange={setField('alcohol_status')} options={ALCOHOL_OPTIONS} />
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-y-3 gap-x-6">
              {[
                ['Smoking', user?.smoking_status],
                ['Alcohol', user?.alcohol_status],
              ].map(([label, val]) => (
                <div key={label}>
                  <p className="text-xs text-slate-600">{label}</p>
                  <p className="text-sm text-slate-300">{val || <span className="text-slate-600 italic">Not set</span>}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* ── MEDICAL INFO ── */}
        <div className="glass-card rounded-3xl p-6 flex flex-col gap-5">
          <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
            <Shield size={15} className="text-teal-400" /> Medical Information
          </h3>

          {editing ? (
            <div className="flex flex-col gap-4">
              <TextareaField
                label="Known Allergies"
                value={form.allergies}
                onChange={setField('allergies')}
                placeholder="e.g. Penicillin, Sulfa drugs, Peanuts..."
              />
              <TextareaField
                label="Current Medications"
                value={form.current_medications}
                onChange={setField('current_medications')}
                placeholder="e.g. Metformin 500mg, Lisinopril 10mg..."
              />
              <div>
                <p className="text-xs font-medium text-slate-400 mb-3">Diagnosed Conditions</p>
                <ConditionSelector
                  selectedIds={selectedIds}
                  customList={customList}
                  onIdsChange={setSelectedIds}
                  onCustomChange={setCustomList}
                />
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4">
              <div>
                <p className="text-xs text-slate-600 mb-1">Allergies</p>
                <p className="text-sm text-slate-300">{user?.allergies || <span className="italic text-slate-600">None recorded</span>}</p>
              </div>
              <div>
                <p className="text-xs text-slate-600 mb-1">Current Medications</p>
                <p className="text-sm text-slate-300">{user?.current_medications || <span className="italic text-slate-600">None recorded</span>}</p>
              </div>
              <div>
                <p className="text-xs text-slate-600 mb-2">Diagnosed Conditions</p>
                {conditions.length === 0 ? (
                  <p className="text-sm text-slate-600 italic">None added</p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {conditions.map((c) => (
                      <span key={c.id} className={`text-xs px-3 py-1.5 rounded-full border ${
                        c.is_custom
                          ? 'bg-violet-500/10 border-violet-500/30 text-violet-300'
                          : 'bg-teal-500/10 border-teal-500/30 text-teal-300'
                      }`}>
                        {c.condition_name}
                        {c.is_custom && <span className="ml-1 opacity-50">(custom)</span>}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Disclaimer */}
        <div className="glass-card rounded-2xl p-4">
          <p className="text-xs text-slate-500 leading-relaxed">
            Your health profile is stored locally in the app database and helps MediBot personalise responses.
            It is never shared with third parties.
          </p>
        </div>

      </div>
    </div>
  )
}
