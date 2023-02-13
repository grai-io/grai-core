import { Box, Stack } from "@mui/material"
import React from "react"
import { useSearchParams } from "react-router-dom"
import StepsControl, { StepsControlOptions } from "./StepsControl"
import SearchControl from "./SearchControl"
import LimitGraphControl from "./LimitGraphControl"

export type ControlOptions = {
  steps?: StepsControlOptions
}

type GraphControlsProps = {
  errors: boolean
  options?: ControlOptions
  search: string | null
  onSearch: (input: string | null) => void
}

const GraphControls: React.FC<GraphControlsProps> = ({
  errors,
  options,
  search,
  onSearch,
}) => {
  let [searchParams, setSearchParams] = useSearchParams()

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && errors

  const set = (input: URLSearchParams, field: string, value: string) => {
    input.set(field, value)

    return input
  }

  const remove = (input: URLSearchParams, field: string) => {
    input.delete(field)

    return input
  }

  const handleToggleLimit = () => {
    setSearchParams(
      limitGraph
        ? remove(searchParams, "limitGraph")
        : set(searchParams, "limitGraph", "true")
    )
  }

  return (
    <Box sx={{ position: "relative" }}>
      <Stack
        spacing={1}
        direction="row"
        sx={{
          position: "absolute",
          top: 10,
          left: 10,
          width: "100%",
          pointerEvents: "all",
          zIndex: 30,
        }}
      >
        {errors && (
          <LimitGraphControl value={limitGraph} onChange={handleToggleLimit} />
        )}
        {options?.steps && <StepsControl options={options.steps} />}
        <SearchControl value={search} onChange={onSearch} />
      </Stack>
    </Box>
  )
}

export default GraphControls
