import React from "react"
import { CheckCircle, ChevronRight } from "@mui/icons-material"
import {
  Stepper,
  Step,
  StepLabel,
  StepIconProps,
  SxProps,
  Theme,
  Box,
} from "@mui/material"
import { WizardSteps } from "./WizardLayout"

function StepIcon(props: StepIconProps) {
  const { active, completed } = props

  if (completed) return <CheckCircle sx={{ color: "#8338EC" }} />

  const borderColor = active ? "#8338EC" : "#EBEBEB"

  return (
    <Box
      sx={{
        width: "20px",
        height: "20px",
        borderRadius: "24px",
        borderColor,
        borderWidth: 2,
        borderStyle: "solid",
        m: "2px",
      }}
    />
  )
}

type WizardStepperProps = {
  steps: WizardSteps
  activeStep: number
  sx?: SxProps<Theme>
}

const WizardStepper: React.FC<WizardStepperProps> = ({
  steps,
  activeStep,
  sx,
}) => {
  const stepTitles = steps.map(step => step.title)

  return (
    <Stepper
      activeStep={activeStep}
      connector={<ChevronRight sx={{ color: "#A7ABB3" }} />}
      sx={{
        ...sx,
        // "& .MuiStep-root": {
        //   border: "1px solid #EBEBEB",
        // },
        // "& .MuiStep-root.Mui-active": {
        //   border: "1px solid #8338EC",
        // },
        // "& .MuiStep-root.Mui-completed": {
        //   border: "1px solid #8338EC",
        // },
      }}
    >
      {stepTitles.map((step, index) => (
        <Step
          key={step}
          sx={{
            borderRadius: "73px",
            border:
              activeStep >= index ? "1px solid #8338EC" : "1px solid #EBEBEB",
            p: "8px",
            pr: "16px",
          }}
        >
          <StepLabel StepIconComponent={StepIcon}>{step}</StepLabel>
        </Step>
      ))}
    </Stepper>
  )
}

export default WizardStepper
