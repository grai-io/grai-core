import React from "react"
import { Refresh } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import { Box, Stack, Tooltip } from "@mui/material"
import useSearchParams from "helpers/useSearchParams"
import FilterControl from "./FilterControl"
import LimitGraphControl from "./LimitGraphControl"
import LoadMoreControl, { LoadMoreControlOptions } from "./LoadMoreControl"
import SearchControl from "./SearchControl"
import StepsControl, { StepsControlOptions } from "./StepsControl"
import { CombinedFilters } from "../useCombinedFilters"

export type ControlOptions = {
  steps?: StepsControlOptions
  loadMore?: LoadMoreControlOptions
}

type GraphControlsProps = {
  errors: boolean
  options?: ControlOptions
  search: string | null
  onSearch: (input: string | null) => void
  onRefresh?: () => void
  loading?: boolean
  combinedFilters: CombinedFilters
}

const GraphControls: React.FC<GraphControlsProps> = ({
  errors,
  options,
  search,
  onSearch,
  onRefresh,
  loading,
  combinedFilters,
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
          right: "24px",
          pointerEvents: "all",
          zIndex: 30,
          display: "flex",
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
          <FilterControl combinedFilters={combinedFilters} />
        </Stack>
        {options?.loadMore && <LoadMoreControl options={options.loadMore} />}
        <Box sx={{ flexGrow: 1 }} />
        {onRefresh && (
          <Tooltip title="Refresh">
            <Box>
              <LoadingButton
                loading={loading}
                onClick={onRefresh}
                variant="outlined"
                sx={{
                  backgroundColor: "white",
                  minWidth: 0,
                  height: "40px",
                  width: "40px",
                }}
              >
                <Refresh />
              </LoadingButton>
            </Box>
          </Tooltip>
        )}
      </Box>
    </Box>
  )
}

export default GraphControls
