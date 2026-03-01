import MealEditor from '../../../components/MealEditor'
import { API_BASE } from '../../../lib/api'

async function loadMeal(id: string) {
  const res = await fetch(`${API_BASE}/api/meals/${id}`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Meal failed')
  return res.json()
}

export default async function MealPage({ params }: { params: { id: string } }) {
  const data = await loadMeal(params.id)
  return (
    <main className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-bold">Meal #{data.meal.id.slice(0, 8)}</h1>
      <img src={`${API_BASE}${data.meal.image_path}`} alt="meal" className="mt-4 w-full rounded" />
      <div className="mt-4">
        <MealEditor initialData={data} />
      </div>
    </main>
  )
}
