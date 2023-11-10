import React, { ReactNode } from "react"
import { ArrowBack } from "@mui/icons-material"
import { Box, Button } from "@mui/material"
import { ElementOptions } from "./WizardLayout"

type WizardBottomBarProps = {
  opts: ElementOptions
  children?: ReactNode
}

const WizardBottomBar: React.FC<WizardBottomBarProps> = ({
  opts,
  children,
}) => (
  <Box sx={{ textAlign: "right", my: 3 }}>
    {opts.activeStep > 0 && (
      <Button
        variant="outlined"
        onClick={opts.backStep}
        startIcon={<ArrowBack />}
        sx={{ mr: 2 }}
      >
        Go Back
      </Button>
    )}

    {children}
  </Box>
)

export default WizardBottomBar
