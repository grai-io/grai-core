import { AppBar, Container, Toolbar, Typography } from "@mui/material"
import React, { ReactNode, useState } from "react"
import WizardAppBar from "./WizardAppBar"
import WizardBottomBar from "./WizardBottomBar"

export type ElementOptions = {
  setActiveStep: (activeStep: number) => void
  forwardStep: () => void
  backStep: () => void
}

export type WizardStep = {
  title: string
  subTitle?: string | ReactNode
  actionText?: string
  actionButtons?: ReactNode | ((opts: ElementOptions) => ReactNode)
  element: ReactNode | ((opts: ElementOptions) => ReactNode)
}

export type WizardSteps = WizardStep[]

type WizardLayoutProps = {
  title: string
  steps: WizardSteps
  closeRoute: (workspaceId?: string) => string
}

const WizardLayout: React.FC<WizardLayoutProps> = ({
  title,
  steps,
  closeRoute,
}) => {
  const [activeStep, setActiveStep] = useState(0)

  const forwardStep = () => setActiveStep(activeStep + 1)
  const backStep = () => setActiveStep(activeStep > 0 ? activeStep - 1 : 0)

  const opts: ElementOptions = {
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
        closeRoute={closeRoute}
      />
      <Toolbar />
      {step.subTitle && (
        <>
          <AppBar position="fixed" color="transparent" elevation={0}>
            <Toolbar />
            <Toolbar
              sx={{
                backgroundColor: theme => theme.palette.grey[100],
                height: 80,
              }}
            >
              <Container maxWidth="lg">
                {typeof step.subTitle === "string" ? (
                  <Typography variant="h5">{step.subTitle}</Typography>
                ) : (
                  step.subTitle
                )}
              </Container>
            </Toolbar>
          </AppBar>
          <Toolbar sx={{ height: 80 }} />
        </>
      )}
      <Container maxWidth="lg">{stepElement}</Container>
      <Toolbar sx={{ height: 80 }} />
      <WizardBottomBar step={step} activeStep={activeStep} opts={opts} />
    </>
  )
}

export default WizardLayout
