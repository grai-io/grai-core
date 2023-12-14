import { useEffect, useState } from "react"

export default function useLocalState<T = any>(
  key: string,
  initial: T,
  preferInitial: boolean = false,
): [T, (value: T) => void] {
  const [value, setValue] = useState<T>(() => {
    if (initial && preferInitial) return initial

    if (typeof window !== "undefined" && window.localStorage) {
      const saved = window.localStorage.getItem(key)
      if (saved) {
        return JSON.parse(saved)
      }
    }

    return initial
  })

  useEffect(() => {
    if (typeof window !== "undefined" && window.localStorage) {
      value !== undefined && value !== null
        ? window.localStorage.setItem(key, JSON.stringify(value))
        : window.localStorage.removeItem(key)
    }
  }, [key, value])

  return [value, setValue]
}
