import React, { ReactNode } from "react"
import { Box } from "@mui/material"
import Loading from "components/layout/Loading"
import PageLayout from "components/layout/PageLayout"
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
    <PageLayout>
      <Box
        sx={{ display: "flex", backgroundColor: "white", minHeight: "100%" }}
      >
        <SettingsDrawer />
        <Box component="main" sx={{ flexGrow: 1 }}>
          {loading && <Loading />}
          {children}
        </Box>
      </Box>
    </PageLayout>
  )
}

export default SettingsLayout
