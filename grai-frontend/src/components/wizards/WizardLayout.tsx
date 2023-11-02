import React, { ReactNode, useState } from "react"
import { Box, Toolbar } from "@mui/material"
import WizardAppBar from "./WizardAppBar"

export type ElementOptions = {
  activeStep: number
  setActiveStep: (activeStep: number) => void
  forwardStep: () => void
  backStep: () => void
}

export type WizardStep = {
  title: string
  element: ReactNode | ((opts: ElementOptions) => ReactNode)
}

export type WizardSteps = WizardStep[]

type WizardLayoutProps = {
  steps: WizardSteps
  className?: string
}

const WizardLayout: React.FC<WizardLayoutProps> = ({ steps, className }) => {
  const [activeStep, setActiveStep] = useState(0)

  const forwardStep = () => setActiveStep(activeStep + 1)
  const backStep = () => setActiveStep(activeStep > 0 ? activeStep - 1 : 0)

  const opts: ElementOptions = {
    activeStep,
    setActiveStep,
    forwardStep,
    backStep,
  }

  const step = steps[activeStep]

  const stepElement =
    typeof step.element === "function" ? step.element(opts) : step.element

  return (
    <Box className={className}>
      <WizardAppBar steps={steps} activeStep={activeStep} />
      <Toolbar />
      <Box sx={{ px: 5 }}>{stepElement}</Box>
    </Box>
  )
}

export default WizardLayout
