import React, { ReactNode } from "react"
import { ArrowBack } from "@mui/icons-material"
import { Toolbar, Container, Box, Button } from "@mui/material"
import { ElementOptions } from "./WizardLayout"

type WizardBottomBarProps = {
  opts: ElementOptions
  children?: ReactNode
}

const WizardBottomBar: React.FC<WizardBottomBarProps> = ({
  opts,
  children,
}) => (
  <Toolbar sx={{ height: 80 }}>
    <Container maxWidth="lg" sx={{ display: "flex" }}>
      <Box sx={{ flexGrow: 1 }}>
        {opts.activeStep > 0 && (
          <Button
            variant="outlined"
            onClick={opts.backStep}
            startIcon={<ArrowBack />}
          >
            Go Back
          </Button>
        )}
      </Box>
      <Box>{children}</Box>
    </Container>
  </Toolbar>
)

export default WizardBottomBar
