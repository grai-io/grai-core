import { Box, Button, Checkbox, Stack } from "@mui/material"
import React from "react"
import { useSearchParams } from "react-router-dom"
import StepsControl, { StepsControlOptions } from "./StepsControl"
import SearchControl from "./SearchControl"

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
          <Box>
            <Button
              variant="contained"
              disableElevation
              onClick={handleToggleLimit}
              sx={{
                backgroundColor: "white",
                color: "black",
                borderStyle: "solid",
                borderWidth: 1,
                borderColor: "divider",
                borderRadius: 0,
                pl: 0,
                pr: 1.5,
                py: 0,
                minWidth: 0,
              }}
            >
              <Checkbox
                sx={{ ml: 0.5, mr: 1, p: 0 }}
                size="small"
                checked={limitGraph}
              />
              Limit Graph
            </Button>
          </Box>
        )}
        {options?.steps && <StepsControl options={options.steps} />}
        <SearchControl value={search} onChange={onSearch} />
      </Stack>
    </Box>
  )
}

export default GraphControls
