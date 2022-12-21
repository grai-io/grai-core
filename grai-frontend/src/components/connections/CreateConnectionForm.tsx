import { gql, useMutation } from "@apollo/client"
import React from "react"
import { useNavigate, useParams } from "react-router-dom"
import ConnectionsForm, { Values } from "./ConnectionsForm"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "./__generated__/CreateConnection"

export const CREATE_CONNECTION = gql`
  mutation CreateConnection(
    $workspaceId: ID!
    $connectorId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON!
  ) {
    createConnection(
      workspaceId: $workspaceId
      connectorId: $connectorId
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
    ) {
      id
      connector {
        id
        name
      }
      namespace
      name
      metadata
      is_active
      created_at
      updated_at
    }
  }
`

const CreateConnectionForm: React.FC = () => {
  const { workspaceId } = useParams()
  const navigate = useNavigate()

  const [createConnection, { loading, error }] = useMutation<
    CreateConnection,
    CreateConnectionVariables
  >(CREATE_CONNECTION)

  const handleSubmit = (values: Values) =>
    createConnection({
      variables: {
        workspaceId: workspaceId ?? "",
        connectorId: values.connector?.id ?? "",
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets,
      },
    }).then(data => navigate(`/workspaces/${workspaceId}/connections`))

  const defaultValues: Values = {
    connector: null,
    namespace: "",
    name: "",
    metadata: null,
    secrets: null,
  }

  return (
    <ConnectionsForm
      defaultValues={defaultValues}
      onSubmit={handleSubmit}
      loading={loading}
      error={error}
    />
  )
}

export default CreateConnectionForm
