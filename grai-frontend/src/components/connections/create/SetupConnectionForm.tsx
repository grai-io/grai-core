import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { LoadingButton } from "@mui/lab"
import { Box, TextField } from "@mui/material"
import Form from "components/form/Form"
import { NewSource } from "components/sources/__generated__/NewSource"
import GraphError from "components/utils/GraphError"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "./__generated__/CreateConnection"
import { NewConnection } from "./__generated__/NewConnection"
import { NewSourceConnection } from "./__generated__/NewSourceConnection"
import {
  UpdateConnectionInitial,
  UpdateConnectionInitialVariables,
} from "./__generated__/UpdateConnectionInitial"
import ConnectionsMetadata from "../ConnectionsMetadata"
import { Connector } from "../connectors/ConnectorCard"

export const CREATE_CONNECTION = gql`
  mutation CreateConnection(
    $workspaceId: ID!
    $connectorId: ID!
    $sourceName: String!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
  ) {
    createConnection(
      workspaceId: $workspaceId
      connectorId: $connectorId
      sourceName: $sourceName
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
    ) {
      id
      connector {
        id
        name
        icon
      }
      source {
        id
        name
      }
      last_run {
        id
        status
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

export const UPDATE_CONNECTION = gql`
  mutation UpdateConnectionInitial(
    $connectionId: ID!
    $sourceName: String!
    $namespace: String!
    $name: String!
    $metadata: JSON!
    $secrets: JSON
  ) {
    updateConnection(
      id: $connectionId
      sourceName: $sourceName
      namespace: $namespace
      name: $name
      metadata: $metadata
      secrets: $secrets
    ) {
      id
      connector {
        id
        name
        icon
      }
      source {
        id
        name
        priority
      }
      last_run {
        id
        status
      }
      namespace
      name
      metadata
      created_at
      updated_at
    }
  }
`

export interface Connection extends Values {
  id: string
}

export type Values = {
  id?: string
  sourceName: string
  namespace: string
  name: string
  metadata: any
  secrets: any
}

type SetupConnectionFormProps = {
  workspaceId: string
  connector: Connector
  connection: Connection | null
  onSubmit: (connection: Connection) => void
  disabled?: boolean
  children?: React.ReactNode
}

const SetupConnectionForm: React.FC<SetupConnectionFormProps> = ({
  workspaceId,
  connector,
  connection,
  onSubmit,
  disabled,
  children,
}) => {
  const [values, setValues] = useState<Values>({
    sourceName: connection?.sourceName ?? connector.name,
    name: connection?.name ?? connector.name,
    namespace: connection?.namespace ?? "default",
    metadata: connection?.metadata,
    secrets: connection?.secrets,
  })

  const [createConnection, { loading: loadingCreate, error: errorCreate }] =
    useMutation<CreateConnection, CreateConnectionVariables>(
      CREATE_CONNECTION,
      {
        update(cache, { data }) {
          cache.modify({
            id: cache.identify({
              id: workspaceId,
              __typename: "Workspace",
            }),
            fields: {
              /* istanbul ignore next */
              connections(existingConnections = { data: [] }) {
                if (!data?.createConnection) return existingConnections

                const newConnection = cache.writeFragment<NewConnection>({
                  data: data.createConnection,
                  fragment: gql`
                    fragment NewConnection on Connection {
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
                  `,
                })
                return {
                  data: [...(existingConnections.data ?? []), newConnection],
                }
              },
            },
          })
          cache.modify({
            id: cache.identify({
              id: workspaceId,
              __typename: "Workspace",
            }),
            fields: {
              /* istanbul ignore next */
              sources(existingSources = { data: [] }) {
                if (!data?.createConnection) return existingSources

                const newConnection = cache.writeFragment<NewSourceConnection>({
                  data: data.createConnection,
                  fragment: gql`
                    fragment NewSourceConnection on Connection {
                      id
                      name
                      connector {
                        id
                        name
                        icon
                      }
                      last_run {
                        id
                        status
                      }
                    }
                  `,
                })

                const existingSource = existingSources.data.find(
                  (s: { id: string }) =>
                    s.id === data.createConnection.source.id,
                )

                if (existingSource) {
                  existingSource.connections.data.push(newConnection)

                  return {
                    data: [
                      ...existingSources.data.filter(
                        (s: { id: string }) =>
                          s.id !== data.createConnection.source.id,
                      ),
                      existingSource,
                    ],
                  }
                }

                const newSource = cache.writeFragment<NewSource>({
                  data: data.createConnection.source,
                  fragment: gql`
                    fragment NewSource on Source {
                      id
                      name
                      priority
                    }
                  `,
                })

                return {
                  data: [...(existingSources.data ?? []), newSource],
                }
              },
            },
          })
        },
      },
    )

  const [updateConnection, { loading: loadingUpdate, error: errorUpdate }] =
    useMutation<UpdateConnectionInitial, UpdateConnectionInitialVariables>(
      UPDATE_CONNECTION,
    )

  const handleSubmit = () => {
    if (connection?.id) {
      updateConnection({
        variables: { ...values, connectionId: connection.id },
      })
        .then(
          ({ data }) =>
            data?.updateConnection &&
            onSubmit({
              ...data.updateConnection,
              sourceName: data.updateConnection.source.name,
              secrets: values.secrets,
            }),
        )
        .catch(() => {})
      return
    }

    createConnection({
      variables: { ...values, workspaceId, connectorId: connector.id },
    })
      .then(
        ({ data }) =>
          data?.createConnection &&
          onSubmit({
            ...data.createConnection,
            sourceName: data.createConnection.source.name,
            secrets: values.secrets,
          }),
      )
      .catch(() => {})
  }

  return (
    <Form onSubmit={handleSubmit}>
      {errorCreate && <GraphError error={errorCreate} />}
      {errorUpdate && <GraphError error={errorUpdate} />}
      <TextField
        label="Source"
        margin="normal"
        value={values.sourceName}
        onChange={event =>
          setValues({ ...values, sourceName: event.target.value })
        }
        required
        fullWidth
      />
      <TextField
        label="Name"
        margin="normal"
        value={values.name}
        onChange={event => setValues({ ...values, name: event.target.value })}
        required
        fullWidth
      />
      <TextField
        label="Namespace"
        margin="normal"
        value={values.namespace}
        onChange={event =>
          setValues({ ...values, namespace: event.target.value })
        }
        required
        fullWidth
      />
      {connector && (
        <ConnectionsMetadata
          connector={connector}
          metadata={values.metadata}
          secrets={values.secrets}
          onChangeMetadata={value => setValues({ ...values, metadata: value })}
          onChangeSecrets={value => setValues({ ...values, secrets: value })}
          edit={!!connection}
        />
      )}
      {children}
      <Box sx={{ textAlign: "right", mt: 2 }}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{
            minWidth: 120,
            backgroundColor: "#FC6016",
            boxShadow: "0px 4px 6px 0px rgba(252, 96, 22, 0.20)",
          }}
          loading={loadingCreate || loadingUpdate}
          disabled={disabled}
        >
          Test Connection
        </LoadingButton>
      </Box>
    </Form>
  )
}

export default SetupConnectionForm
