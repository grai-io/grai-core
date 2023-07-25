import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { ArrowForward } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import { Grid, TextField } from "@mui/material"
import Form from "components/form/Form"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import {
  CreateConnection,
  CreateConnectionVariables,
} from "./__generated__/CreateConnection"
import { NewConnection } from "./__generated__/NewConnection"
import {
  UpdateConnectionInitial,
  UpdateConnectionInitialVariables,
} from "./__generated__/UpdateConnectionInitial"
import ConnectionFile from "./ConnectionFile"
import ConnectorComingSoon from "./ConnectorComingSoon"
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
      temp: true
    ) {
      id
      connector {
        id
        name
      }
      source {
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
      }
      source {
        id
        name
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

type SetupConnectionProps = {
  workspaceId: string
  opts: ElementOptions
  connector: Connector
  connection: Connection | null
  setConnection: (connection: Connection) => void
}

const SetupConnection: React.FC<SetupConnectionProps> = ({
  workspaceId,
  opts,
  connector,
  connection,
  setConnection,
}) => {
  const [values, setValues] = useState<Values>(
    connection ?? {
      sourceName: connector.name,
      name: connector.name,
      namespace: "default",
      metadata: {},
      secrets: {},
    },
  )

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
                if (!data?.createConnection) return

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
        },
      },
    )

  const [updateConnection, { loading: loadingUpdate, error: errorUpdate }] =
    useMutation<UpdateConnectionInitial, UpdateConnectionInitialVariables>(
      UPDATE_CONNECTION,
    )

  const handleSubmit = () =>
    connection?.id
      ? updateConnection({
          variables: { ...values, connectionId: connection.id },
        })
          .then(
            ({ data }) =>
              data?.updateConnection &&
              setConnection({
                ...data.updateConnection,
                sourceName: data.updateConnection.source.name,
                secrets: values.secrets,
              }),
          )
          .then(() => opts.forwardStep())
          .catch(() => {})
      : createConnection({
          variables: { ...values, workspaceId, connectorId: connector.id },
        })
          .then(
            ({ data }) =>
              data?.createConnection &&
              setConnection({
                ...data.createConnection,
                sourceName: data.createConnection.source.name,
                secrets: values.secrets,
              }),
          )
          .then(() => opts.forwardStep())
          .catch(() => {})

  if (connector.coming_soon)
    return <ConnectorComingSoon connector={connector} opts={opts} />

  if (connector.metadata?.file?.name)
    return (
      <ConnectionFile
        connector={connector}
        workspaceId={workspaceId}
        opts={opts}
      />
    )

  return (
    <Form onSubmit={handleSubmit}>
      <WizardSubtitle
        title={`Connect to ${connector.name}`}
        icon={connector.icon}
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
              setValues({ ...values, sourceName: event.target.value })
            }
            required
            fullWidth
          />
          <TextField
            label="Name"
            margin="normal"
            value={values.name}
            onChange={event =>
              setValues({ ...values, name: event.target.value })
            }
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
              onChangeMetadata={value =>
                setValues({ ...values, metadata: value })
              }
              onChangeSecrets={value =>
                setValues({ ...values, secrets: value })
              }
            />
          )}
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
        >
          Continue
        </LoadingButton>
      </WizardBottomBar>
    </Form>
  )
}

export default SetupConnection
