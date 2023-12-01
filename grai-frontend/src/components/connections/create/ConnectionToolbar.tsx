import React from "react"
import { ChevronLeft } from "@mui/icons-material"
import { Box, Divider, IconButton, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import WizardStepper from "components/wizards/WizardStepper"

const steps = ["Select Integration", "Setup Connection", "Set Schedule"]

type ConnectionToolbarProps = {
  title: string
  onBack: string | (() => void)
  activeStep: number
}

const ConnectionToolbar: React.FC<ConnectionToolbarProps> = ({
  title,
  activeStep,
  onBack,
}) => (
  <>
    <Box sx={{ p: "24px", display: "flex", alignItems: "center" }}>
      <Box sx={{ flexGrow: 1, display: "flex", alignItems: "center" }}>
        {typeof onBack === "string" ? (
          <IconButton component={Link} to={onBack}>
            <ChevronLeft sx={{ color: "#A8ADAF" }} />
          </IconButton>
        ) : (
          <IconButton onClick={onBack}>
            <ChevronLeft sx={{ color: "#A8ADAF" }} />
          </IconButton>
        )}

        <Typography
          sx={{ color: "#1F2A37", fontSize: 22, fontWeight: 800 }}
          variant="h6"
        >
          {title}
        </Typography>
      </Box>
      <WizardStepper
        steps={steps}
        activeStep={activeStep}
        sx={{ flexGrow: 1 }}
      />
      <Box sx={{ flexGrow: 1 }} />
    </Box>
    <Divider />
  </>
)

export default ConnectionToolbar
