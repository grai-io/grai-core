import React, { ReactNode } from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import ErrorBoundary from "components/utils/ErrorBoundary"
import {
  GetWorkspacePageLayout,
  GetWorkspacePageLayoutVariables,
} from "./__generated__/GetWorkspacePageLayout"
import AppDrawer from "./AppDrawer"
import GettingStarted from "./GettingStarted"
import Loading from "./Loading"

export const GET_WORKSPACE = gql`
  query GetWorkspacePageLayout(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
      runs(filters: { action: TESTS }) {
        meta {
          filtered
        }
      }
      nodes(filters: { node_type: { equals: "Table" } }) {
        meta {
          filtered
        }
      }
      connections {
        meta {
          total
        }
      }
    }
  }
`

type PageLayoutProps = {
  children?: ReactNode
  loading?: boolean
  padding?: boolean
}

const PageLayout: React.FC<PageLayoutProps> = ({
  children,
  loading,
  padding,
}) => {
  const { organisationName, workspaceName } = useWorkspace()

  const { data } = useQuery<
    GetWorkspacePageLayout,
    GetWorkspacePageLayoutVariables
  >(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  const hasConnections = (data?.workspace.connections.meta.total ?? 0) > 0

  return (
    <>
      {data && !hasConnections && <GettingStarted />}
      <Box sx={{ display: "flex" }}>
        <AppDrawer />
        <Box sx={{ width: "100%" }}>
          {loading && <Loading />}
          <ErrorBoundary>
            <Box
              sx={{
                padding: padding ? 3 : undefined,
                flexGrow: 1,
                backgroundColor: "#F8F8F8",
                minHeight: "calc(100vh - 64px)",
              }}
            >
              {children}
            </Box>
          </ErrorBoundary>
        </Box>
      </Box>
    </>
  )
}

export default PageLayout
