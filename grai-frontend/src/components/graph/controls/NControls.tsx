import { Remove, Add } from "@mui/icons-material"
import { Box, Typography, Button } from "@mui/material"
import React from "react"

export type ControlNOptions = {
  value: number
  setValue: (input: number) => void
}

type NControlsProps = {
  options: ControlNOptions
}

const NControls: React.FC<NControlsProps> = ({ options }) => (
  <Box sx={{ display: "flex" }}>
    <Typography variant="body2" sx={{ p: 0.5, ml: 1, mr: 0.5 }}>
      N
    </Typography>
    <Button
      variant="contained"
      disableElevation
      onClick={() => options.setValue(Math.max(options.value - 1, 1))}
      disabled={options.value < 2}
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
    <Typography
      variant="body2"
      sx={{
        backgroundColor: "white",
        color: "black",
        borderStyle: "solid",
        borderWidth: 1,
        borderColor: "divider",
        borderRadius: 0,
        borderRight: "none",
        p: 0.25,
        textAlign: "center",
        minWidth: 25,
      }}
    >
      {options.value}
    </Typography>
    <Button
      variant="contained"
      disableElevation
      onClick={() => options.setValue(options.value + 1)}
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
      <Add fontSize="small" />
    </Button>
  </Box>
)

export default NControls
