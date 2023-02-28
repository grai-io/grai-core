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
      width: 25,
      minWidth: 30,
      height: 30,
      p: 0.5,
      position: "absolute",
      left: position === "left" ? -29 : null,
      right: position === "right" ? -29 : null,
      top: "calc(50% - 15px)",
      backgroundColor: "white",
      borderRadius: 0,
      borderColor: "rgb(85, 85, 85)",
    }}
  >
    <Add />
  </Button>
)

export default HiddenTableButton
