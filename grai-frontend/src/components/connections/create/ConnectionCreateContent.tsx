import React from "react"
import NotFound from "pages/NotFound"
import useSearchParams from "helpers/useSearchParams"
import ConnectorSelectTab from "components/connections/create/ConnectorSelectTab"
import ScheduleTab from "./ScheduleTab"
import SetupConnectionTab from "./SetupConnectionTab"
import UpdateConnectionTab from "./UpdateConnectionTab"

interface Workspace {
  id: string
}

type ConnectionCreateContentProps = {
  workspace: Workspace
}

const ConnectionCreateContent: React.FC<ConnectionCreateContentProps> = ({
  workspace,
}) => {
  const { searchParams } = useSearchParams()

  const step = searchParams.get("step")
  const connectionId = searchParams.get("connectionId")

  if (step === "schedule") {
    if (!connectionId) return <NotFound />

    return (
      <ScheduleTab workspaceId={workspace.id} connectionId={connectionId} />
    )
  }

  if (connectionId)
    return (
      <UpdateConnectionTab
        workspaceId={workspace.id}
        connectionId={connectionId}
      />
    )

  const connectorId = searchParams.get("connectorId")

  if (connectorId)
    return (
      <SetupConnectionTab
        workspaceId={workspace.id}
        connectorId={connectorId}
      />
    )

  return <ConnectorSelectTab />
}

export default ConnectionCreateContent
