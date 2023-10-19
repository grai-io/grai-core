import React from "react"
import { Box } from "@mui/material"
import GitHubInstallation from "components/settings/installations/GitHubInstallation"
import SettingsAppBar from "components/settings/SettingsAppBar"
import SettingsLayout from "components/settings/SettingsLayout"

const Installations: React.FC = () => (
  <SettingsLayout>
    <SettingsAppBar title="Installations" />
    <Box sx={{ p: 3, pl: "48px" }}>
      <GitHubInstallation />
    </Box>
  </SettingsLayout>
)

export default Installations
