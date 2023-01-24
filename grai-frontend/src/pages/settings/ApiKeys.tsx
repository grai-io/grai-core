import { gql, useQuery } from "@apollo/client"
import { Box } from "@mui/material"
import React from "react"
import ApiKeysHeader from "components/settings/apiKeys/ApiKeysHeader"
import ApiKeysTable from "components/settings/apiKeys/ApiKeysTable"
import SettingsLayout from "components/settings/SettingsLayout"
import { GetApiKeys, GetApiKeysVariables } from "./__generated__/GetApiKeys"
import GraphError from "components/utils/GraphError"
import useWorkspace from "helpers/useWorkspace"
import NotFound from "pages/NotFound"

const GET_API_KEYS = gql`
  query GetApiKeys($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organsationName, name: $workspaceName) {
      id
      api_keys {
        id
        name
        prefix
        created
        revoked
        expiry_date
        created_by {
          id
          username
        }
      }
    }
  }
`

const ApiKeys: React.FC = () => {
  const { organisationName, workspaceName } = useWorkspace()

  const { loading, error, data } = useQuery<GetApiKeys, GetApiKeysVariables>(
    GET_API_KEYS,
    {
      variables: {
        organisationName,
        workspaceName,
      },
    }
  )

  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!workspace) return <NotFound />

  return (
    <SettingsLayout>
      <Box sx={{ p: 3 }}>
        <ApiKeysHeader workspaceId={workspace.id} />
        <ApiKeysTable
          keys={data?.workspace?.api_keys ?? []}
          loading={loading}
        />
      </Box>
    </SettingsLayout>
  )
}

export default ApiKeys
