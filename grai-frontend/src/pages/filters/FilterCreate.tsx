import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box, Typography } from "@mui/material"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import CreateFilter from "components/filters/CreateFilter"
import Loading from "components/layout/Loading"
import PageLayout from "components/layout/PageLayout"
import GraphError from "components/utils/GraphError"

export const GET_WORKSPACE = gql`
  query GetWorkspaceFilterCreate(
    $organisationName: String!
    $workspaceName: String!
  ) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      name
    }
  }
`

const FilterCreate: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery(GET_WORKSPACE, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <PageLayout>
      <Box sx={{ p: 3 }}>
        <Typography variant="h6">Create Filter</Typography>
        <CreateFilter workspaceId={workspace.id} />
      </Box>
    </PageLayout>
  )
}

export default FilterCreate
