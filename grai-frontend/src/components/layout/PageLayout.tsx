import React, { ReactNode } from "react"
import { Box } from "@mui/material"
import ErrorBoundary from "components/utils/ErrorBoundary"
import AppDrawer from "./AppDrawer"
import GettingStarted from "./GettingStarted"
import { User } from "./profile/Profile"
import SampleData, { Workspace } from "./SampleData"

type PageLayoutProps = {
  children?: ReactNode
  gettingStarted?: boolean
  sampleData?: boolean
  workspace?: Workspace
  profile?: User
}

const PageLayout: React.FC<PageLayoutProps> = ({
  children,
  gettingStarted,
  sampleData,
  workspace,
  profile,
}) => (
  <>
    {gettingStarted && <GettingStarted />}
    {sampleData && workspace && <SampleData workspace={workspace} />}
    <Box sx={{ display: "flex" }}>
      <AppDrawer profile={profile} sampleData={sampleData && !!workspace} />
      <Box sx={{ flexGrow: 1 }}>
        <ErrorBoundary>
          <Box
            sx={{
              backgroundColor: "#F8F8F8",
              height: "100%",
              minHeight:
                !gettingStarted && !sampleData ? "100vh" : "calc(100vh - 64px)",
            }}
          >
            {children}
          </Box>
        </ErrorBoundary>
      </Box>
    </Box>
  </>
)

export default PageLayout
