import {
  NavigateOptions,
  URLSearchParamsInit,
  useSearchParams as baseUseSearchParams,
} from "react-router-dom"

type SetURLSearchParams = (
  nextInit?:
    | URLSearchParamsInit
    | ((prev: URLSearchParams) => URLSearchParamsInit),
  navigateOpts?: NavigateOptions
) => void

export const set = (
  input: URLSearchParams,
  field: string,
  value: string | boolean
) => {
  input.set(field, typeof value === "string" ? value : value ? "true" : "false")

  return input
}

export const remove = (input: URLSearchParams, field: string) => {
  input.delete(field)

  return input
}

const useSearchParams = (): {
  searchParams: URLSearchParams
  setSearchParams: SetURLSearchParams
  setSearchParam: (
    field: string,
    value: string | boolean | null | undefined,
    clear?: boolean | null
  ) => void
} => {
  let [searchParams, setSearchParams] = baseUseSearchParams()

  const setSearchParam = (
    field: string,
    value: string | boolean | null | undefined,
    clear: boolean | null = null
  ) =>
    setSearchParams(
      clear || !value
        ? remove(searchParams, field)
        : set(searchParams, field, value)
    )

  return { searchParams, setSearchParams, setSearchParam }
}

export default useSearchParams
