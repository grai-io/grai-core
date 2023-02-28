import React from "react"
import { Remove, Add } from "@mui/icons-material"
import { Box, Button, TextField, InputAdornment } from "@mui/material"

export type StepsControlOptions = {
  value: number
  setValue: (input: number) => void
}

type StepsControlProps = {
  options: StepsControlOptions
}

const StepsControl: React.FC<StepsControlProps> = ({ options }) => (
  <Box sx={{ display: "flex" }}>
    <TextField
      value={options.value}
      onChange={event => options.setValue(Number(event.target.value))}
      size="small"
      sx={{
        backgroundColor: "white",
        width: 100,
        "& fieldset": {
          borderRadius: "4px 0px 0px 4px",
        },
      }}
      inputProps={{
        style: {
          textAlign: "right",
          borderTopRightRadius: 0,
          borderBottomRightRadius: 0,
          borderRadius: 0,
        },
      }}
      InputProps={{
        startAdornment: <InputAdornment position="start">Steps</InputAdornment>,
      }}
    />
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
        borderColor: "rgba(0,0,0,0.23)",
        borderRadius: 0,
        borderLeft: "none",
        p: 0.25,
        minWidth: 40,
      }}
    >
      <Remove fontSize="small" />
    </Button>
    <Button
      variant="contained"
      disableElevation
      onClick={() => options.setValue(options.value + 1)}
      sx={{
        backgroundColor: "white",
        color: "black",
        borderStyle: "solid",
        borderWidth: 1,
        borderColor: "rgba(0,0,0,0.23)",
        borderRadius: "0px 4px 4px 0px",
        borderLeft: "none",
        p: 0.25,
        minWidth: 40,
      }}
    >
      <Add fontSize="small" />
    </Button>
  </Box>
)

export default StepsControl
