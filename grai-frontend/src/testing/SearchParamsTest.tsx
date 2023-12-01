import React, { useEffect } from "react"
import useSearchParams from "helpers/useSearchParams"

type SearchParamsTestProps = {
  onSearchParams: (searchParams: URLSearchParams) => void
}

const SearchParamsTest: React.FC<SearchParamsTestProps> = ({
  onSearchParams,
}) => {
  const { searchParams } = useSearchParams()

  useEffect(() => {
    onSearchParams(searchParams)
  }, [onSearchParams, searchParams])

  return null
}

export default SearchParamsTest
