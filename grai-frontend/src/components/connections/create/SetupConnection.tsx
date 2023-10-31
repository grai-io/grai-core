import React, { useState } from "react"
import { gql, useMutation } from "@apollo/client"
import GraphError from "components/utils/GraphError"
import { ElementOptions } from "components/wizards/WizardLayout"
import {
  ValidateConnection as ValidateConnectionType,
  ValidateConnectionVariables,
} from "./__generated__/ValidateConnection"
import ConnectionFile from "./ConnectionFile"
import ConnectorComingSoon from "./ConnectorComingSoon"
import { Connection } from "./CreateConnectionWizard"
import SetupConnectionForm from "./SetupConnectionForm"
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
  const [run, setRun] = useState<Run | null>(null)
  const [validated, setValidated] = useState(false)

  const [createRun, { loading, error }] = useMutation<
    ValidateConnectionType,
    ValidateConnectionVariables
  >(CREATE_RUN)

  if (connector.status === "coming_soon")
    return <ConnectorComingSoon connector={connector} opts={opts} />

  if (connector.metadata?.file?.name)
    return (
      <ConnectionFile
        connector={connector}
        workspaceId={workspaceId}
        opts={opts}
      />
    )

  const handleSubmit = (connection: Connection) => {
    setRun(null)
    setValidated(false)
    setConnection(connection)

    createRun({
      variables: {
        connectionId: connection.id,
      },
    }).then(data => data.data?.runConnection && setRun(data.data.runConnection))
  }

  const handleContinue = () => opts.forwardStep()

  return (
    <SetupConnectionForm
      workspaceId={workspaceId}
      opts={opts}
      connector={connector}
      connection={connection}
      onSubmit={handleSubmit}
      onContinue={handleContinue}
      disabled={!validated && (loading || !!run)}
      validated={validated}
    >
      {run && (
        <ValidateConnection
          workspaceId={workspaceId}
          run={run}
          onValidate={() => setValidated(true)}
        />
      )}
      {error && <GraphError error={error} />}
    </SetupConnectionForm>
  )
}

export default SetupConnection
