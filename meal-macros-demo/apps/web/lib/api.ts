const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

export async function analyzeMeal(file: File) {
  const formData = new FormData()
  formData.append('image', file)
  const res = await fetch(`${API_BASE}/api/meals/analyze`, { method: 'POST', body: formData })
  if (!res.ok) throw new Error('Analyze failed')
  return res.json()
}

export async function searchFoods(q: string) {
  const res = await fetch(`${API_BASE}/api/foods/search?q=${encodeURIComponent(q)}`)
  if (!res.ok) throw new Error('Search failed')
  return res.json()
}

export async function confirmMeal(payload: any) {
  const res = await fetch(`${API_BASE}/api/meals/confirm`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Confirm failed')
  return res.json()
}

export async function getMeal(id: string) {
  const res = await fetch(`${API_BASE}/api/meals/${id}`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Meal load failed')
  return res.json()
}

export { API_BASE }
