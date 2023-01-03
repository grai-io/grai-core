import React, { ReactNode } from "react"
import AppTopBar from "./AppTopBar"
import Loading from "./Loading"

type PageLayoutProps = {
  children?: ReactNode
  loading?: boolean
}

const PageLayout: React.FC<PageLayoutProps> = ({ children, loading }) => (
  <>
    <AppTopBar />
    {loading && <Loading />}
    {children}
  </>
)

export default PageLayout
