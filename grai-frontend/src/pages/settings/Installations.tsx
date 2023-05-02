import React from "react"
import { Box, Typography } from "@mui/material"
import GitHubInstallation from "components/settings/installations/GitHubInstallation"
import SettingsLayout from "components/settings/SettingsLayout"

const Installations: React.FC = () => (
  <SettingsLayout>
    <Box sx={{ p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3 }}>
        Installations
      </Typography>
      <GitHubInstallation />
    </Box>
  </SettingsLayout>
)

export default Installations
