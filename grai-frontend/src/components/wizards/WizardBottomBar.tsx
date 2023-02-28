import React, { ReactNode } from "react"
import { ArrowBack } from "@mui/icons-material"
import {
  AppBar,
  Toolbar,
  Container,
  Typography,
  Box,
  Button,
} from "@mui/material"
import { ElementOptions } from "./WizardLayout"

type WizardBottomBarProps = {
  actionText?: string
  opts: ElementOptions
  children?: ReactNode
}

const WizardBottomBar: React.FC<WizardBottomBarProps> = ({
  actionText,
  opts,
  children,
}) => (
  <>
    <Toolbar sx={{ height: 80 }} />
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
          <Box>
            {actionText && (
              <Typography
                sx={{
                  fontSize: 16,
                  color: theme => theme.palette.grey[500],
                  fontWeight: 500,
                }}
              >
                {actionText}
              </Typography>
            )}

            {children}
          </Box>
        </Container>
      </Toolbar>
    </AppBar>
  </>
)

export default WizardBottomBar
