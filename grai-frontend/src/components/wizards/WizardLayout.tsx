import React, { ReactNode, useState } from "react"
import { Container, Toolbar } from "@mui/material"
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
  title: string
  steps: WizardSteps
  onClose: () => void
}

const WizardLayout: React.FC<WizardLayoutProps> = ({
  title,
  steps,
  onClose,
}) => {
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
    <>
      <WizardAppBar
        title={title}
        steps={steps}
        activeStep={activeStep}
        onClose={onClose}
      />
      <Toolbar />
      <Container maxWidth="lg">{stepElement}</Container>
    </>
  )
}

export default WizardLayout
