import React from "react"
import { Box, Stack } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"
import FilterControl from "./FilterControl"
import LimitGraphControl from "./LimitGraphControl"
import LoadMoreControl, { LoadMoreControlOptions } from "./LoadMoreControl"
import SearchControl from "./SearchControl"
import StepsControl, { StepsControlOptions } from "./StepsControl"

export type ControlOptions = {
  steps?: StepsControlOptions
  loadMore?: LoadMoreControlOptions
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
      <Box
        sx={{
          position: "absolute",
          top: "24px",
          left: "24px",
          pointerEvents: "all",
          zIndex: 30,
        }}
      >
        <Stack spacing={1} direction="row">
          {errors && (
            <LimitGraphControl
              value={limitGraph}
              onChange={handleToggleLimit}
            />
          )}
          {options?.steps && <StepsControl options={options.steps} />}
          <SearchControl value={search} onChange={onSearch} />
          <FilterControl />
        </Stack>
        {options?.loadMore && <LoadMoreControl options={options.loadMore} />}
      </Box>
    </Box>
  )
}

export default GraphControls
