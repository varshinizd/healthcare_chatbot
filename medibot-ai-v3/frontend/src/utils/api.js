const BASE_URL = import.meta.env.VITE_API_URL || ''

function getToken() {
  return localStorage.getItem('medibot_token')
}

function authHeaders() {
  const token = getToken()
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  }
}

async function handleResponse(res) {
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

// ── Auth ────────────────────────────────────────────────────────────────────

export async function signup(data) {
  const res = await fetch(`${BASE_URL}/auth/signup`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse(res)
}

export async function login(data) {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  return handleResponse(res)
}

export async function fetchMe() {
  const res = await fetch(`${BASE_URL}/auth/me`, { headers: authHeaders() })
  return handleResponse(res)
}

export async function updateProfile(data) {
  const res = await fetch(`${BASE_URL}/auth/profile`, {
    method: 'PUT',
    headers: authHeaders(),
    body: JSON.stringify(data),
  })
  return handleResponse(res)
}

export async function fetchConditionsList() {
  const res = await fetch(`${BASE_URL}/auth/conditions`)
  return handleResponse(res)
}

// ── Chat ────────────────────────────────────────────────────────────────────

export async function sendChatMessage({ message, sessionId }) {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ message, session_id: sessionId }),
  })
  return handleResponse(res)
}

export async function submitFeedback({ sessionId, messageId, score, comment }) {
  const res = await fetch(`${BASE_URL}/feedback`, {
    method: 'POST',
    headers: authHeaders(),
    body: JSON.stringify({ session_id: sessionId, message_id: messageId, score, comment: comment || null }),
  })
  return res.json()
}

export async function fetchHealth() {
  const res = await fetch(`${BASE_URL}/health`)
  return res.json()
}
