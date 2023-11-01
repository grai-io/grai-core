import React from "react"
import { Box, Divider, Toolbar, Typography } from "@mui/material"
import { WizardSteps } from "./WizardLayout"
import WizardStepper from "./WizardStepper"

type WizardAppBarProps = {
  title?: string
  steps: WizardSteps
  activeStep: number
}

const WizardAppBar: React.FC<WizardAppBarProps> = ({
  title,
  steps,
  activeStep,
}) => (
  <Box>
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flex: 1 }}>
        {title}
      </Typography>

      <WizardStepper steps={steps} activeStep={activeStep} sx={{ flex: 2 }} />

      <Box sx={{ flex: 1 }} />
    </Toolbar>
    <Divider />
  </Box>
)

export default WizardAppBar
