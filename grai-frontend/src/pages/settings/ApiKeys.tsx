import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import React from "react"
import { useParams } from "react-router-dom"
import ApiKeysHeader from "components/settings/apiKeys/ApiKeysHeader"
import ApiKeysTable from "components/settings/apiKeys/ApiKeysTable"
import SettingsLayout from "components/settings/SettingsLayout"
import { GetApiKeys, GetApiKeysVariables } from "./__generated__/GetApiKeys"

const GET_API_KEYS = gql`
  query GetApiKeys($workspaceId: ID!) {
    workspace(pk: $workspaceId) {
      id
      apiKeys {
        id
        name
        prefix
        created
        revoked
        expiryDate
        createdBy {
          id
          username
        }
      }
    }
  }
`

const ApiKeys: React.FC = () => {
  const { workspaceId } = useParams()

  const { loading, error, data } = useQuery<GetApiKeys, GetApiKeysVariables>(
    GET_API_KEYS,
    {
      variables: {
        workspaceId: workspaceId ?? "",
      },
    }
  )

  if (error) return <p>Error : {error.message}</p>

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <ApiKeysHeader />
        <ApiKeysTable keys={data?.workspace?.apiKeys ?? []} loading={loading} />
      </Box>
    </SettingsLayout>
  )
}

export default ApiKeys
