import { gql, useMutation } from "@apollo/client"
import React from "react"
import ConnectionsForm, { Values } from "../ConnectionsForm"
import {
  UpdateConnection,
  UpdateConnectionVariables,
} from "./__generated__/UpdateConnection"

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnection(
    $connectionId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
    $schedules: JSON
    $is_active: Boolean
  ) {
    updateConnection(
      id: $connectionId
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
      schedules: $schedules
      is_active: $is_active
    ) {
      id
      namespace
      name
      metadata
      is_active
      created_at
      updated_at
    }
  }
`

interface Connector {
  id: string
  name: string
  metadata: any
}

export interface Connection {
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
        namespace: values.namespace,
        name: values.name,
        metadata: values.metadata,
        secrets: values.secrets ?? {},
        schedules: null,
        is_active: true,
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
