import React, { ReactNode } from "react"
import { Box } from "@mui/material"
import ErrorBoundary from "components/utils/ErrorBoundary"
import AppTopBar from "./AppTopBar"
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
  <>
    <AppTopBar />
    {loading && <Loading />}
    <ErrorBoundary>
      <Box sx={{ padding: padding ? 3 : undefined }}>{children}</Box>
    </ErrorBoundary>
  </>
)

export default PageLayout
