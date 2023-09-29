import React from "react"
import { gql, useQuery } from "@apollo/client"
import NotFound from "pages/NotFound"
import useWorkspace from "helpers/useWorkspace"
import ApiKeysHeader from "components/settings/apiKeys/ApiKeysHeader"
import ApiKeysTable from "components/settings/apiKeys/ApiKeysTable"
import SettingsContent from "components/settings/SettingsContent"
import SettingsLayout from "components/settings/SettingsLayout"
import GraphError from "components/utils/GraphError"
import { GetApiKeys, GetApiKeysVariables } from "./__generated__/GetApiKeys"

export const GET_API_KEYS = gql`
  query GetApiKeys($organisationName: String!, $workspaceName: String!) {
    workspace(organisationName: $organisationName, name: $workspaceName) {
      id
      api_keys {
        data {
          id
          name
          prefix
          created
          revoked
          expiry_date
          created_by {
            id
            username
            first_name
            last_name
          }
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
    },
  )

  if (error) return <GraphError error={error} />

  const workspace = data?.workspace

  if (!loading && !workspace) return <NotFound />

  return (
    <SettingsLayout>
      <ApiKeysHeader workspaceId={workspace?.id} />
      <SettingsContent>
        <ApiKeysTable
          keys={workspace?.api_keys.data ?? []}
          loading={loading}
          workspaceId={workspace?.id}
        />
      </SettingsContent>
    </SettingsLayout>
  )
}

export default ApiKeys
