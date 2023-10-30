import { Chip } from "@mui/material"
import React from "react"

type SetupIncompleteProps = {
  size?: "small" | "medium"
}

const SetupIncomplete: React.FC<SetupIncompleteProps> = ({ size }) => (
  <Chip
    label="Setup Incomplete"
    color="warning"
    size={size}
    sx={{
      fontWeight: 600,
      borderRadius: "100px",
      fontSize: "14px",
      mr: 2,
    }}
  />
)

export default SetupIncomplete
