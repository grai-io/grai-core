import React from "react"
import { Close } from "@mui/icons-material"
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material"
import { WizardSteps } from "./WizardLayout"
import WizardStepper from "./WizardStepper"

type WizardAppBarProps = {
  title: string
  steps: WizardSteps
  activeStep: number
  onClose: () => void
}

const WizardAppBar: React.FC<WizardAppBarProps> = ({
  title,
  steps,
  activeStep,
  onClose,
}) => (
  <AppBar
    position="fixed"
    color="transparent"
    elevation={0}
    sx={{
      borderBottomStyle: "solid",
      borderBottomWidth: 1,
      borderBottomColor: "divider",
      zIndex: theme => theme.zIndex.drawer + 1,
      backgroundColor: "white",
    }}
  >
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flex: 1 }}>
        {title}
      </Typography>

      <WizardStepper steps={steps} activeStep={activeStep} sx={{ flex: 2 }} />

      <Box sx={{ flex: 1, textAlign: "right" }}>
        <IconButton onClick={onClose}>
          <Close />
        </IconButton>
      </Box>
    </Toolbar>
  </AppBar>
)

export default WizardAppBar
