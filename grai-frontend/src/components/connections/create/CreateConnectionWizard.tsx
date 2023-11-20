import React, { useState } from "react"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import PageHeader from "components/layout/PageHeader"
import WizardLayout, { WizardSteps } from "components/wizards/WizardLayout"
import ConnectorSelectTab from "./ConnectorSelectTab"
import SetSchedule from "./SetSchedule"
import SetupConnection from "./SetupConnection"
import { Values } from "./SetupConnectionForm"
import { Connector } from "../connectors/ConnectorCard"

export interface Connection extends Values {
  id: string
}

type CreateConnectionWizardProps = {
  workspaceId: string
}

const CreateConnectionWizard: React.FC<CreateConnectionWizardProps> = ({
  workspaceId,
}) => {
  const { workspaceNavigate } = useWorkspace()

  const [connector, setConnector] = useState<Connector | null>(null)
  const [connection, setConnection] = useState<Connection | null>(null)

  const handleSelect =
    (setActiveStep: (step: number) => void) => (connector: Connector) => {
      setConnector(connector)
      setActiveStep(1)
    }

  const steps: WizardSteps = [
    {
      title: "Select integration",
      element: opts => (
        <ConnectorSelectTab
          opts={opts}
          onSelect={handleSelect(opts.setActiveStep)}
        />
      ),
    },
    {
      title: "Setup connection",
      element: opts =>
        connector && (
          <SetupConnection
            workspaceId={workspaceId}
            connector={connector}
            connection={connection}
            setConnection={setConnection}
            opts={opts}
          />
        ),
    },
    {
      title: "Set schedule",
      element: opts =>
        connection && (
          <SetSchedule
            opts={opts}
            connection={connection}
            onComplete={() =>
              connection && workspaceNavigate(`connections/${connection.id}`)
            }
          />
        ),
    },
  ]

  return (
    <>
      <PageHeader title="Add Source" />
      <PageContent noPadding>
        <WizardLayout steps={steps} className="create-connection-wizard" />
      </PageContent>
    </>
  )
}

export default CreateConnectionWizard
