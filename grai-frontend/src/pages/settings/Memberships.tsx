import React from "react"
import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"
import MembershipsHeader from "components/settings/memberships/MembershipsHeader"
import MembershipsTable from "components/settings/memberships/MembershipsTable"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
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

  const workspace = data?.workspace

  if (!loading && !workspace) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <MembershipsHeader workspaceId={workspace?.id} />
        <MembershipsTable
          memberships={data?.workspace?.memberships ?? []}
          loading={loading}
          workspaceId={workspace?.id}
        />
      </Box>
    </SettingsLayout>
  )
}

export default Memberships
