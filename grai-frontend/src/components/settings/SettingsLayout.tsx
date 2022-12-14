import { Box, Toolbar } from "@mui/material"
import React, { ReactNode } from "react"
import SettingsAppBar from "./SettingsAppBar"
import SettingsDrawer from "./SettingsDrawer"

type SettingsLayoutProps = {
  children?: ReactNode
}

const SettingsLayout: React.FC<SettingsLayoutProps> = ({ children }) => {
  return (
    <Box sx={{ display: "flex" }}>
      <SettingsAppBar />
      <SettingsDrawer />
      <Box component="main" sx={{ flexGrow: 1 }}>
        <Toolbar />
        {children}
      </Box>
    </Box>
  )
}

export default SettingsLayout
