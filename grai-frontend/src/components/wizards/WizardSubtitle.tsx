import React, { ReactNode } from "react"
import { AppBar, Toolbar, Container, Typography, Box } from "@mui/material"

type WizardSubtitleProps = {
  title?: string | null
  icon?: string | null
  children?: ReactNode
}

const WizardSubtitle: React.FC<WizardSubtitleProps> = ({
  title,
  icon,
  children,
}) => (
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
          {
            <Box sx={{ display: "flex" }}>
              {icon && (
                <img
                  src={icon}
                  alt={`${title} logo`}
                  style={{ height: 28, width: 28 }}
                />
              )}
              {title && (
                <Typography variant="h5" sx={{ ml: icon ? 2 : undefined }}>
                  {title}
                </Typography>
              )}
            </Box>
          }
          {children}
        </Container>
      </Toolbar>
    </AppBar>
    <Toolbar sx={{ height: 80 }} />
  </>
)

export default WizardSubtitle
