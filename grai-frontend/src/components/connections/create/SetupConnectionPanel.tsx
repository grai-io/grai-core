import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import { Grid } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import GraphError from "components/utils/GraphError"
import {
  ValidateConnection as ValidateConnectionType,
  ValidateConnectionVariables,
} from "./__generated__/ValidateConnection"
import ConnectorToolbar from "./ConnectorToolbar"
import CreateConnectionHelp from "./CreateConnectionHelp"
import RunError from "./RunError"
import SetupConnectionForm, { Connection } from "./SetupConnectionForm"
import ValidateConnection from "./ValidateConnection"
import { Connector } from "../connectors/ConnectorCard"

export const CREATE_RUN = gql`
  mutation ValidateConnection($connectionId: ID!) {
    runConnection(connectionId: $connectionId, action: VALIDATE) {
      id
    }
  }
`

interface Run {
  id: string
  status?: string
  metadata?: any
}

type SetupConnectionPanelProps = {
  workspaceId: string
  connector: Connector
  defaultConnection: Connection | null
}

const SetupConnectionPanel: React.FC<SetupConnectionPanelProps> = ({
  workspaceId,
  connector,
  defaultConnection,
}) => {
  const { workspaceNavigate } = useWorkspace()

  const [run, setRun] = useState<Run | null>(null)
  const [connection, setConnection] = useState<Connection | null>(
    defaultConnection,
  )

  const [createRun, { loading, error }] = useMutation<
    ValidateConnectionType,
    ValidateConnectionVariables
  >(CREATE_RUN)

  const handleSubmit = (connection: Connection) => {
    setRun(null)
    setConnection(connection)

    createRun({
      variables: {
        connectionId: connection.id,
      },
    })
      .then(data => data.data?.runConnection && setRun(data.data.runConnection))
      .catch(() => {})
  }

  const handleSuccess = () => {
    setTimeout(
      () =>
        workspaceNavigate(
          `connections/create?connectionId=${connection?.id}&step=schedule`,
        ),
      1000,
    )
  }

  return (
    <>
      <ConnectorToolbar connector={connector} />
      <Grid container>
        <Grid item md={6}>
          <PageContent>
            <SetupConnectionForm
              workspaceId={workspaceId}
              connector={connector}
              connection={connection}
              onSubmit={handleSubmit}
              disabled={loading || (run ? !run.status : false)}
            >
              {error && <GraphError error={error} />}
              {run?.metadata && <RunError run={run} />}
            </SetupConnectionForm>
          </PageContent>
        </Grid>
        <Grid item md={6}>
          {run && !run.status ? (
            <PageContent sx={{ height: "calc(100% - 48px)" }}>
              <ValidateConnection
                workspaceId={workspaceId}
                run={run}
                onSuccess={handleSuccess}
                onFail={setRun}
                detailed
              />
            </PageContent>
          ) : (
            <PageContent sx={{ maxHeight: "calc(100% - 48px)" }}>
              <CreateConnectionHelp connector={connector} />
            </PageContent>
          )}
        </Grid>
      </Grid>
    </>
  )
}

export default SetupConnectionPanel
