import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import PageLayout from "components/layout/PageLayout"
import MembershipsHeader from "components/settings/memberships/MembershipsHeader"
import MembershipsTable from "components/settings/memberships/MembershipsTable"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import React from "react"
import {
  GetMemberships,
  GetMembershipsVariables,
} from "./__generated__/GetMemberships"

export const GET_MEMBERSHIPS = gql`
  query GetMemberships($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      memberships {
        id
        role
        user {
          id
          username
          first_name
          last_name
        }
        is_active
        created_at
      }
    }
  }
`

const Memberships: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<
    GetMemberships,
    GetMembershipsVariables
  >(GET_MEMBERSHIPS, {
    variables: {
      organisationName,
      workspaceName,
    },
  })

  if (error) return <GraphError error={error} />
  if (loading) return <PageLayout loading />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <MembershipsHeader workspaceId={workspace.id} />
        <MembershipsTable
          memberships={data?.workspace?.memberships ?? []}
          loading={loading}
        />
      </Box>
    </SettingsLayout>
  )
}

export default Memberships
