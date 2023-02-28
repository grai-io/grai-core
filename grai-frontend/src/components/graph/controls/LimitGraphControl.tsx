import React from "react"
import { Box, Button, Checkbox, Typography } from "@mui/material"

type LimitGraphControlProps = {
  value: boolean
  onChange: (value: boolean) => void
}

const LimitGraphControl: React.FC<LimitGraphControlProps> = ({
  value,
  onChange,
}) => (
  <Box>
    <Button
      variant="outlined"
      disableElevation
      onClick={() => onChange(!value)}
      sx={{
        backgroundColor: "white",
        borderColor: "rgba(0,0,0,0.23)",
        color: "rgba(0, 0, 0, 0.6)",
        pl: 0.5,
        pr: 1.5,
        minWidth: 0,
        height: 40,
      }}
    >
      <Checkbox sx={{ ml: 0.5, mr: 1, p: 0 }} size="small" checked={value} />
      <Typography>Limit Graph</Typography>
    </Button>
  </Box>
)

export default LimitGraphControl
