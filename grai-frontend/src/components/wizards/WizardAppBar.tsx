import { Close } from "@mui/icons-material"
import { AppBar, Box, IconButton, Toolbar, Typography } from "@mui/material"
import React from "react"
import { useNavigate, useParams } from "react-router-dom"
import { WizardSteps } from "./WizardLayout"
import WizardStepper from "./WizardStepper"

type WizardAppBarProps = {
  title: string
  steps: WizardSteps
  activeStep: number
  closeRoute: (workspaceId?: string) => string
}

const WizardAppBar: React.FC<WizardAppBarProps> = ({
  title,
  steps,
  activeStep,
  closeRoute,
}) => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const handleClose = () => navigate(closeRoute(workspaceId))

  return (
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
          <IconButton onClick={handleClose}>
            <Close />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  )
}

export default WizardAppBar
