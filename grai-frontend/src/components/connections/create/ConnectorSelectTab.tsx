import React from "react"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import ConnectorSelect from "./ConnectorSelect"
import { Connector } from "../connectors/ConnectorCard"

type ConnectorSelectTabProps = {
  opts: ElementOptions
  onSelect: (connector: Connector) => void
}

const ConnectorSelectTab: React.FC<ConnectorSelectTabProps> = ({
  opts,
  onSelect,
}) => (
  <>
    <WizardSubtitle title="Select an integration" />
    <ConnectorSelect onSelect={onSelect} />
    <WizardBottomBar
      opts={opts}
      actionText="Click on an integration to continue"
    />
  </>
)

export default ConnectorSelectTab
