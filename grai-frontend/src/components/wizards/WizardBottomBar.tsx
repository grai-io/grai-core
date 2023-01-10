import { ArrowBack } from "@mui/icons-material"
import {
  AppBar,
  Toolbar,
  Container,
  Typography,
  Box,
  Button,
} from "@mui/material"
import React from "react"
import { ElementOptions, WizardStep } from "./WizardLayout"

type WizardBottomBarProps = {
  step: WizardStep
  activeStep: number
  opts: ElementOptions
}

const WizardBottomBar: React.FC<WizardBottomBarProps> = ({
  step,
  activeStep,
  opts,
}) => (
  <AppBar
    position="fixed"
    color="transparent"
    elevation={0}
    sx={{
      top: "auto",
      bottom: 0,
      borderTopStyle: "solid",
      borderTopWidth: 1,
      borderTopColor: "divider",
      backgroundColor: "white",
    }}
  >
    <Toolbar sx={{ height: 80 }}>
      <Container maxWidth="lg" sx={{ display: "flex" }}>
        <Box sx={{ flexGrow: 1 }}>
          {activeStep > 0 && (
            <Button
              variant="outlined"
              onClick={opts.backStep}
              startIcon={<ArrowBack />}
            >
              Go Back
            </Button>
          )}
        </Box>
        <Box>
          <Typography
            sx={{
              fontSize: 16,
              color: theme => theme.palette.grey[500],
              fontWeight: 500,
            }}
          >
            {step.actionText}
          </Typography>
          {typeof step.actionButtons === "function"
            ? step.actionButtons(opts)
            : step.actionButtons}
        </Box>
      </Container>
    </Toolbar>
  </AppBar>
)

export default WizardBottomBar
