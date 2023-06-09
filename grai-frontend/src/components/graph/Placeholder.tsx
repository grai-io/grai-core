import React from "react"
import { Box } from "@mui/material"

const Placeholder: React.FC = () => (
  <Box
    data-testid="placeholder"
    sx={{
      background: theme => theme.palette.grey[200],
      height: "16px",
      m: 3,
    }}
  />
)

export default Placeholder
