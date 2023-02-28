import React from "react"
import { CheckCircle } from "@mui/icons-material"
import {
  Stepper,
  Step,
  StepLabel,
  StepConnector,
  stepConnectorClasses,
  StepIconProps,
  styled,
  SxProps,
  Theme,
} from "@mui/material"
import { WizardSteps } from "./WizardLayout"

const QontoConnector = styled(StepConnector)(({ theme }) => ({
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    top: 10,
    left: "calc(-50% + 16px)",
    right: "calc(50% + 16px)",
  },
  [`&.${stepConnectorClasses.active}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: theme.palette.secondary.main,
    },
  },
  [`&.${stepConnectorClasses.completed}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: theme.palette.secondary.main,
    },
  },
  [`& .${stepConnectorClasses.line}`]: {
    borderColor:
      theme.palette.mode === "dark" ? theme.palette.grey[800] : "#eaeaf0",
    borderTopWidth: 1,
    borderRadius: 1,
    marginLeft: 10,
    marginRight: 10,
  },
}))

const QontoStepIconRoot = styled("div")<{ ownerState: { active?: boolean } }>(
  ({ theme, ownerState }) => ({
    color: theme.palette.mode === "dark" ? theme.palette.grey[700] : "#eaeaf0",
    display: "flex",
    height: 22,
    alignItems: "center",
    ...(ownerState.active && {
      color: theme.palette.secondary.main,
    }),
    "& .QontoStepIcon-completedIcon": {
      color: theme.palette.secondary.main,
      zIndex: 1,
      fontSize: 18,
    },
    "& .QontoStepIcon-circle": {
      width: 14,
      height: 14,
      borderRadius: "50%",
      backgroundColor: ownerState.active ? "currentColor" : "white",
      borderColor: theme.palette.secondary.main,
      borderWidth: 1,
      borderStyle: "solid",
    },
  })
)

function QontoStepIcon(props: StepIconProps) {
  const { active, completed, className } = props

  return (
    <QontoStepIconRoot ownerState={{ active }} className={className}>
      {completed ? (
        <CheckCircle className="QontoStepIcon-completedIcon" />
      ) : (
        <div className="QontoStepIcon-circle" />
      )}
    </QontoStepIconRoot>
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
    <Stepper activeStep={activeStep} connector={<QontoConnector />} sx={sx}>
      {stepTitles.map(step => (
        <Step key={step}>
          <StepLabel StepIconComponent={QontoStepIcon}>{step}</StepLabel>
        </Step>
      ))}
    </Stepper>
  )
}

export default WizardStepper
