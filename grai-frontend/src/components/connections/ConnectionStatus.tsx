import React from "react"
import ConnectorIcon, { Connector } from "components/connectors/ConnectorIcon"
import RunStatus, { Run } from "components/runs/RunStatus"
import SetupIncomplete from "components/sources/SetupIncomplete"

interface Connection {
  validated: boolean
  last_run: Run | null
  connector: Connector
}

type ConnectionStatusProps = {
  connection: Connection
}

const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ connection }) => (
  <>
    {!connection.validated && <SetupIncomplete />}
    {connection.last_run && (
      <RunStatus run={connection.last_run} link sx={{ mr: 3 }} />
    )}
    <ConnectorIcon connector={connection.connector} />
  </>
)

export default ConnectionStatus
