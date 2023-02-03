import { Add, FitScreen, Remove } from "@mui/icons-material"
import { Box, Button, Checkbox, Stack } from "@mui/material"
import React from "react"
import { useSearchParams } from "react-router-dom"
import { useReactFlow } from "reactflow"
import NControls, { ControlNOptions } from "./NControls"

export type ControlOptions = {
  n?: ControlNOptions
}

type GraphControlsProps = {
  errors: boolean
  options?: ControlOptions
}

const GraphControls: React.FC<GraphControlsProps> = ({ errors, options }) => {
  const reactFlowInstance = useReactFlow()
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
          width: 500,
          pointerEvents: "all",
          zIndex: 30,
        }}
      >
        <Box>
          <Button
            variant="contained"
            disableElevation
            onClick={() => reactFlowInstance.zoomIn()}
            sx={{
              backgroundColor: "white",
              color: "black",
              borderStyle: "solid",
              borderWidth: 1,
              borderColor: "divider",
              borderRadius: 0,
              borderRight: "none",
              p: 0.25,
              minWidth: 0,
            }}
          >
            <Add fontSize="small" />
          </Button>
          <Button
            variant="contained"
            disableElevation
            onClick={() => reactFlowInstance.zoomOut()}
            sx={{
              backgroundColor: "white",
              color: "black",
              borderStyle: "solid",
              borderWidth: 1,
              borderColor: "divider",
              borderRadius: 0,
              borderRight: "none",
              p: 0.25,
              minWidth: 0,
            }}
          >
            <Remove fontSize="small" />
          </Button>
          <Button
            variant="contained"
            disableElevation
            onClick={() => reactFlowInstance.fitView()}
            sx={{
              backgroundColor: "white",
              color: "black",
              borderStyle: "solid",
              borderWidth: 1,
              borderColor: "divider",
              borderRadius: 0,
              p: 0.25,
              minWidth: 0,
            }}
          >
            <FitScreen fontSize="small" />
          </Button>
        </Box>
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
        {options?.n && <NControls options={options.n} />}
      </Stack>
    </Box>
  )
}

export default GraphControls
