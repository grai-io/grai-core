import React, { ReactNode } from "react"
import { Box } from "@mui/material"
import ErrorBoundary from "components/utils/ErrorBoundary"
import AppDrawer from "./AppDrawer"
import Loading from "./Loading"

type PageLayoutProps = {
  children?: ReactNode
  loading?: boolean
  padding?: boolean
}

const PageLayout: React.FC<PageLayoutProps> = ({
  children,
  loading,
  padding,
}) => (
  <Box sx={{ display: "flex" }}>
    <AppDrawer />
    {loading && <Loading />}
    <ErrorBoundary>
      <Box
        sx={{
          padding: padding ? 3 : undefined,
          flexGrow: 1,
          backgroundColor: "#F8F8F8",
          minHeight: "100vh",
        }}
      >
        {children}
      </Box>
    </ErrorBoundary>
  </Box>
)

export default PageLayout
