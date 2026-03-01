'use client'

import { useMemo, useState } from 'react'
import { confirmMeal, searchFoods } from '../lib/api'

type Item = any

function scaleNutrients(perGram: Record<string, number>, grams: number) {
  const out: Record<string, number> = {}
  Object.keys(perGram).forEach((k) => (out[k] = (perGram[k] || 0) * grams))
  return out
}

export default function MealEditor({ initialData }: { initialData: any }) {
  const [items, setItems] = useState<Item[]>(initialData.items)
  const [swapTarget, setSwapTarget] = useState<string | null>(null)
  const [results, setResults] = useState<any[]>([])
  const [query, setQuery] = useState('')

  const totals = useMemo(() => {
    const keys = Object.keys(items[0]?.nutrients || {})
    const sum: Record<string, number> = {}
    keys.forEach((k) => (sum[k] = 0))
    items.forEach((it) => keys.forEach((k) => (sum[k] += it.nutrients[k] || 0)))
    return sum
  }, [items])

  const onSlider = (id: string, mult: number) => {
    setItems((prev) =>
      prev.map((it) => {
        if (it.id !== id) return it
        const grams = it.grams_estimated * mult
        return { ...it, portion_multiplier: mult, nutrients: scaleNutrients(it.per_gram_nutrients, grams), grams_display: grams }
      }),
    )
  }

  const onSearch = async () => {
    const data = await searchFoods(query)
    setResults(data.results || [])
  }

  const applySwap = async (cand: any) => {
    if (!swapTarget) return
    setItems((prev) =>
      prev.map((it) =>
        it.id === swapTarget
          ? {
              ...it,
              fdc_match: { ...it.fdc_match, fdc_id: cand.fdc_id, description: cand.description },
              // keep per-gram until confirm; demo keeps UX minimal
            }
          : it,
      ),
    )
    setSwapTarget(null)
  }

  const onConfirm = async () => {
    const payload = {
      meal_id: initialData.meal.id,
      items: items.map((it) => ({
        item_id: it.id,
        fdc_id: it.fdc_match?.fdc_id,
        grams_final: (it.grams_display || it.grams_estimated * it.portion_multiplier || it.grams_estimated),
      })),
    }
    const saved = await confirmMeal(payload)
    setItems(saved.items)
    alert('Meal confirmed')
  }

  return (
    <div className="space-y-4">
      <p className="text-sm text-amber-700">{initialData.disclaimer}</p>
      {items.map((item) => (
        <div key={item.id} className="rounded border bg-white p-4">
          <div className="flex justify-between">
            <div>
              <p className="font-semibold">{item.name_guess}</p>
              <p className="text-xs text-slate-600">{item.fdc_match?.description || 'No USDA match'}</p>
            </div>
            <button className="text-red-600" onClick={() => setItems((p) => p.filter((x) => x.id !== item.id))}>Remove</button>
          </div>
          <div className="mt-2 flex gap-2">
            <button className="rounded bg-slate-200 px-2 py-1 text-xs" onClick={() => { setSwapTarget(item.id); setQuery(item.name_guess); }}>Swap</button>
            <label className="text-xs">Portion {(item.portion_multiplier || 1).toFixed(2)}x</label>
            <input type="range" min="0.5" max="2" step="0.1" value={item.portion_multiplier || 1} onChange={(e) => onSlider(item.id, Number(e.target.value))} />
          </div>
          <p className="mt-2 text-sm">kcal {Math.round(item.nutrients.kcal)} • P {item.nutrients.protein_g.toFixed(1)}g • C {item.nutrients.carbs_g.toFixed(1)}g • F {item.nutrients.fat_g.toFixed(1)}g</p>
        </div>
      ))}

      {swapTarget && (
        <div className="rounded border bg-white p-4">
          <p className="font-semibold">Swap food entry</p>
          <div className="mt-2 flex gap-2">
            <input className="border p-1" value={query} onChange={(e) => setQuery(e.target.value)} />
            <button className="rounded bg-blue-600 px-2 py-1 text-white" onClick={onSearch}>Search</button>
          </div>
          <div className="mt-2 space-y-1">
            {results.map((r) => (
              <button key={r.fdc_id} className="block w-full rounded border p-2 text-left" onClick={() => applySwap(r)}>{r.description} ({r.dataType})</button>
            ))}
          </div>
        </div>
      )}

      <div className="rounded border bg-white p-4">
        <p className="font-semibold">Totals</p>
        <p>Calories: {Math.round(totals.kcal || 0)}</p>
        <p>Protein: {(totals.protein_g || 0).toFixed(1)} g</p>
        <p>Carbs: {(totals.carbs_g || 0).toFixed(1)} g</p>
        <p>Fat: {(totals.fat_g || 0).toFixed(1)} g</p>
      </div>
      <button className="rounded bg-emerald-700 px-4 py-2 text-white" onClick={onConfirm}>Confirm meal</button>
    </div>
  )
}
