'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { analyzeMeal } from '../lib/api'

export default function HomePage() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) return
    setLoading(true)
    setError(null)
    try {
      const data = await analyzeMeal(file)
      localStorage.setItem('lastMealId', data.meal.id)
      router.push(`/meal/${data.meal.id}`)
    } catch {
      setError('Failed to analyze meal.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-2xl p-6">
      <h1 className="text-2xl font-bold">Meal Macros Demo</h1>
      <p className="mt-1 text-sm text-slate-600">Upload a plated meal photo to estimate meal components and nutrients.</p>
      <form className="mt-6 space-y-4 rounded border bg-white p-4" onSubmit={onSubmit}>
        <input type="file" accept="image/*" capture="environment" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button className="rounded bg-blue-600 px-4 py-2 text-white" disabled={!file || loading}>{loading ? 'Analyzing...' : 'Analyze meal'}</button>
        {error && <p className="text-red-600">{error}</p>}
      </form>
    </main>
  )
}
