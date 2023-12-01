import React from "react"
import ConnectionFile from "./ConnectionFile"
import ConnectorComingSoon from "./ConnectorComingSoon"
import { Connection } from "./SetupConnectionForm"
import SetupConnectionPanel from "./SetupConnectionPanel"
import { Connector } from "../connectors/ConnectorCard"

type SetupConnectionProps = {
  workspaceId: string
  connector: Connector
  connection: Connection | null
}

const SetupConnection: React.FC<SetupConnectionProps> = ({
  workspaceId,
  connector,
  connection,
}) => {
  if (connector.status === "coming_soon")
    return <ConnectorComingSoon connector={connector} />

  if (connector.metadata?.file?.name)
    return <ConnectionFile connector={connector} workspaceId={workspaceId} />

  return (
    <SetupConnectionPanel
      workspaceId={workspaceId}
      connector={connector}
      defaultConnection={connection}
    />
  )
}

export default SetupConnection
