import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { useSnackbar } from "notistack"
import GraphError from "components/utils/GraphError"
import {
  UpdateConnection,
  UpdateConnectionVariables,
} from "./__generated__/UpdateConnection"
import {
  ValidateConnectionUpdate,
  ValidateConnectionUpdateVariables,
} from "./__generated__/ValidateConnectionUpdate"
import ConnectionsForm, { Values } from "../ConnectionsForm"
import ValidateConnection from "../create/ValidateConnection"

export const CREATE_RUN = gql`
  mutation ValidateConnectionUpdate($connectionId: ID!) {
    runConnection(connectionId: $connectionId, action: VALIDATE) {
      id
    }
  }
`

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnection(
    $connectionId: ID!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
    $schedules: JSON
    $is_active: Boolean!
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

interface Run {
  id: string
}

export interface Workspace {
  id: string
}

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
  workspace: Workspace
}

const UpdateConnectionForm: React.FC<UpdateConnectionFormProps> = ({
  connection,
  workspace,
}) => {
  const [run, setRun] = useState<Run | null>(null)
  const { enqueueSnackbar } = useSnackbar()

  const [updateConnection, { loading, error }] = useMutation<
    UpdateConnection,
    UpdateConnectionVariables
  >(UPDATE_CONNECTION)

  const [createRun, { error: runError }] = useMutation<
    ValidateConnectionUpdate,
    ValidateConnectionUpdateVariables
  >(CREATE_RUN, {
    variables: {
      connectionId: connection.id,
    },
  })

  const handleSubmit = (values: Values) => {
    setRun(null)
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
      .then(() => enqueueSnackbar("Connection updated"))
      .then(() =>
        createRun().then(
          res => res.data?.runConnection && setRun(res.data.runConnection),
        ),
      )
      .catch(() => {})
  }

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
    >
      {run && <ValidateConnection workspaceId={workspace.id} run={run} />}
      {runError && <GraphError error={runError} />}
    </ConnectionsForm>
  )
}

export default UpdateConnectionForm
