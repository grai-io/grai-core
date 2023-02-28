import React from "react"
import Tabs, { Tab } from "components/tabs/Tabs"
import ConnectionConfiguration from "./configuration/ConnectionConfiguration"
import { Connection as BaseConnection } from "./configuration/UpdateConnectionForm"
import ConnectionRunsTable, { Run } from "./runs/ConnectionRunsTable"
import { Connection as ScheduleConnection } from "./schedule/ConnectionSchedule"
import EditScheduleForm from "./schedule/EditScheduleForm"

interface Connection extends BaseConnection, ScheduleConnection {
  runs: Run[]
}

type ConnectionTabsProps = {
  connection: Connection
}

const ConnectionTabs: React.FC<ConnectionTabsProps> = ({ connection }) => {
  const tabs: Tab[] = [
    {
      value: "runs",
      label: "Runs",
      element: <ConnectionRunsTable runs={connection.runs} />,
    },
    {
      value: "configuration",
      label: "Configuration",
      element: <ConnectionConfiguration connection={connection} />,
    },
    {
      value: "schedule",
      label: "Schedule",
      element: <EditScheduleForm connection={connection} />,
    },
    {
      value: "activity",
      label: "Activity",
      disabled: true,
    },
    {
      value: "alerts",
      label: "Alerts",
      disabled: true,
    },
  ]

  return <Tabs tabs={tabs} />
}

export default ConnectionTabs
