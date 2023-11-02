import React from "react"
import { Box, Divider } from "@mui/material"
import { WizardSteps } from "./WizardLayout"
import WizardStepper from "./WizardStepper"

type WizardAppBarProps = {
  steps: WizardSteps
  activeStep: number
}

const WizardAppBar: React.FC<WizardAppBarProps> = ({ steps, activeStep }) => (
  <>
    <Box sx={{ p: "24px", display: "flex", justifyContent: "center" }}>
      <WizardStepper steps={steps} activeStep={activeStep} />
    </Box>
    <Divider />
  </>
)

export default WizardAppBar
