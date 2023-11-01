import React from "react"
import { Close } from "@mui/icons-material"
import { Box, Divider, IconButton, Toolbar, Typography } from "@mui/material"
import { WizardSteps } from "./WizardLayout"
import WizardStepper from "./WizardStepper"

type WizardAppBarProps = {
  title?: string
  steps: WizardSteps
  activeStep: number
  onClose?: () => void
}

const WizardAppBar: React.FC<WizardAppBarProps> = ({
  title,
  steps,
  activeStep,
  onClose,
}) => (
  <Box>
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flex: 1 }}>
        {title}
      </Typography>

      <WizardStepper steps={steps} activeStep={activeStep} sx={{ flex: 2 }} />

      <Box sx={{ flex: 1, textAlign: "right" }}>
        {onClose && (
          <IconButton onClick={onClose}>
            <Close />
          </IconButton>
        )}
      </Box>
    </Toolbar>
    <Divider />
  </Box>
)

export default WizardAppBar
