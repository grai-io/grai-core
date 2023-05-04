import React from "react"
import { Add } from "@mui/icons-material"
import { Button } from "@mui/material"

type HiddenTableButtonProps = {
  position: "left" | "right"
  onClick?: () => void
}

const HiddenTableButton: React.FC<HiddenTableButtonProps> = ({
  position,
  onClick,
}) => (
  <Button
    variant="outlined"
    onClick={onClick}
    sx={{
      zIndex: 20,
      width: 40,
      minWidth: 40,
      height: 40,
      position: "absolute",
      left: position === "left" ? -48 : null,
      right: position === "right" ? -48 : null,
      top: "calc(50% - 20px)",
      border: "1px solid rgba(131, 56, 236, 0.24)",
      borderRadius: "8px",
      boxShadow: "0px 4px 6px rgba(131, 56, 236, 0.1)",
      backgroundColor: "white",
    }}
  >
    <Add sx={{ color: "#8338EC" }} />
  </Button>
)

export default HiddenTableButton
