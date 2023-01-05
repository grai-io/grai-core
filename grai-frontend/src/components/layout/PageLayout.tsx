import { Box } from "@mui/material"
import React, { ReactNode } from "react"
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
    <Box sx={{ padding: padding ? 3 : undefined }}>{children}</Box>
  </>
)

export default PageLayout
