import { gql, useMutation } from "@apollo/client"
import React from "react"
import ConnectionsForm, { Values } from "./ConnectionsForm"
import {
  UpdateConnection,
  UpdateConnectionVariables,
} from "./__generated__/UpdateConnection"

const UPDATE_CONNECTION = gql`
  mutation UpdateConnection(
    $connectionId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON!
  ) {
    updateConnection(
      id: $connectionId
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
    ) {
      id
      namespace
      name
      metadata
      isActive
      createdAt
      updatedAt
    }
  }
`

interface Connector {
  id: string
  name: string
  metadata: any
}

interface Connection {
  id: string
  namespace: string
  name: string
  metadata: any
  connector: Connector
}

type UpdateConnectionFormProps = {
  connection: Connection
}

const UpdateConnectionForm: React.FC<UpdateConnectionFormProps> = ({
  connection,
}) => {
  const [updateConnection, { loading, error }] = useMutation<
    UpdateConnection,
    UpdateConnectionVariables
  >(UPDATE_CONNECTION)

  const handleSubmit = (values: Values) =>
    updateConnection({
      variables: {
        connectionId: connection.id,
        namespace: values.namespace ?? "",
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets ?? {},
      },
    })

  const defaultValues: Values = {
    connector: connection.connector,
    namespace: connection.namespace,
    name: connection.name,
    metadata: connection.metadata,
    secrets: null,
  }

  return (
    <ConnectionsForm
      defaultValues={defaultValues}
      onSubmit={handleSubmit}
      loading={loading}
      error={error}
      edit
    />
  )
}

export default UpdateConnectionForm
