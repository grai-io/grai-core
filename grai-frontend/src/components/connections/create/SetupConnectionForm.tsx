import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { ArrowForward } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import { Grid, TextField } from "@mui/material"
import Form from "components/form/Form"
import { NewSource } from "components/sources/__generated__/NewSource"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
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
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Connection } from "./CreateConnectionWizard"
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
  opts: ElementOptions
  connector: Connector
  connection: Connection | null
  onSubmit: (connection: Connection) => void
  onContinue: () => void
  disabled?: boolean
  validated: boolean
  children?: React.ReactNode
}

const SetupConnectionForm: React.FC<SetupConnectionFormProps> = ({
  workspaceId,
  opts,
  connector,
  connection,
  onSubmit,
  onContinue,
  disabled,
  validated,
  children,
}) => {
  const [dirty, setDirty] = useState(false)
  const [values, setValues] = useState<Values>(
    connection ?? {
      sourceName: connector.name,
      name: connector.name,
      namespace: "default",
      metadata: {},
      secrets: {},
    },
  )

  const handleChange = (values: Values) => {
    setDirty(true)
    setValues(values)
  }

  /* istanbul ignore next */
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
    if (validated && !dirty) {
      onContinue()
      return
    }

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
        .then(() => setDirty(false))
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
      .then(() => setDirty(false))
      .catch(() => {})
  }

  return (
    <Form onSubmit={handleSubmit}>
      <WizardSubtitle
        title="Setup connection"
        subTitle="Configure the connection to your source"
      />
      {errorCreate && <GraphError error={errorCreate} />}
      {errorUpdate && <GraphError error={errorUpdate} />}
      <Grid container sx={{ mt: 5 }}>
        <Grid item md={8} sx={{ pr: 3 }}>
          <TextField
            label="Source"
            margin="normal"
            value={values.sourceName}
            onChange={event =>
              handleChange({ ...values, sourceName: event.target.value })
            }
            required
            fullWidth
          />
          <TextField
            label="Name"
            margin="normal"
            value={values.name}
            onChange={event =>
              handleChange({ ...values, name: event.target.value })
            }
            required
            fullWidth
          />
          <TextField
            label="Namespace"
            margin="normal"
            value={values.namespace}
            onChange={event =>
              handleChange({ ...values, namespace: event.target.value })
            }
            required
            fullWidth
          />
          {connector && (
            <ConnectionsMetadata
              connector={connector}
              metadata={values.metadata}
              secrets={values.secrets}
              onChangeMetadata={value =>
                handleChange({ ...values, metadata: value })
              }
              onChangeSecrets={value =>
                handleChange({ ...values, secrets: value })
              }
            />
          )}
          {children}
        </Grid>
        <Grid item md={4} sx={{}}>
          <CreateConnectionHelp connector={connector} />
        </Grid>
      </Grid>
      <WizardBottomBar opts={opts}>
        <LoadingButton
          variant="contained"
          type="submit"
          sx={{ minWidth: 120 }}
          endIcon={<ArrowForward />}
          loading={loadingCreate || loadingUpdate}
          disabled={!dirty && disabled}
        >
          Continue
        </LoadingButton>
      </WizardBottomBar>
    </Form>
  )
}

export default SetupConnectionForm
