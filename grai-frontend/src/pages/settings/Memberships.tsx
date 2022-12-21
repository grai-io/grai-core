import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import MembershipsHeader from "components/settings/memberships/MembershipsHeader"
import MembershipsTable from "components/settings/memberships/MembershipsTable"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import React from "react"
import { useParams } from "react-router-dom"
import {
  GetMemberships,
  GetMembershipsVariables,
} from "./__generated__/GetMemberships"

export const GET_MEMBERSHIPS = gql`
  query GetMemberships($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      memberships {
        id
        role
        user {
          id
          username
        }
        createdAt
      }
    }
  }
`

const Memberships: React.FC = () => {
  const { workspaceId } = useParams()

  const { loading, error, data } = useQuery<
    GetMemberships,
    GetMembershipsVariables
  >(GET_MEMBERSHIPS, {
    variables: {
      workspaceId: workspaceId ?? "",
    },
  })

  if (error) return <GraphError error={error} />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <MembershipsHeader />
        <MembershipsTable
          memberships={data?.workspace?.memberships ?? []}
          loading={loading}
        />
      </Box>
    </SettingsLayout>
  )
}

export default Memberships
