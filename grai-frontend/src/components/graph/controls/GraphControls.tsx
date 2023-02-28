import React from "react"
import { Box, Stack } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"
import LimitGraphControl from "./LimitGraphControl"
import SearchControl from "./SearchControl"
import StepsControl, { StepsControlOptions } from "./StepsControl"

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
  const { searchParams, setSearchParam } = useSearchParams()

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true" && errors

  const handleToggleLimit = () => setSearchParam("limitGraph", !limitGraph)

  return (
    <Box sx={{ position: "relative" }}>
      <Stack
        spacing={1}
        direction="row"
        sx={{
          position: "absolute",
          top: 10,
          left: 10,
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
