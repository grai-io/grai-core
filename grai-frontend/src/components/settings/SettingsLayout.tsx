import React, { ReactNode } from "react"
import { Box, Toolbar } from "@mui/material"
import Loading from "components/layout/Loading"
import SettingsAppBar from "./SettingsAppBar"
import SettingsDrawer from "./SettingsDrawer"

type SettingsLayoutProps = {
  children?: ReactNode
  loading?: boolean
}

const SettingsLayout: React.FC<SettingsLayoutProps> = ({
  children,
  loading,
}) => {
  return (
    <Box sx={{ display: "flex" }}>
      <SettingsAppBar />
      <SettingsDrawer />
      <Box component="main" sx={{ flexGrow: 1 }}>
        <Toolbar />
        {loading && <Loading />}
        {children}
      </Box>
    </Box>
  )
}

export default SettingsLayout
