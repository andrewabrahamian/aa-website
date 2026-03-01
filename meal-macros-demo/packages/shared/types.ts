export type Nutrients = {
  kcal: number
  protein_g: number
  carbs_g: number
  fat_g: number
  fiber_g: number
  sugar_g: number
  sodium_mg: number
  potassium_mg: number
  calcium_mg: number
  iron_mg: number
  vitamin_c_mg: number
  vitamin_a_ug_rae: number
}

export type MealItem = {
  id: string
  name_guess: string
  grams_estimated: number
  portion_multiplier: number
  nutrients: Nutrients
  per_gram_nutrients: Nutrients
  fdc_match: {
    fdc_id: number | null
    description: string | null
    dataType?: string | null
    candidates: { fdc_id: number; description: string; dataType?: string }[]
  }
}
