import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import React from "react"
import { Connector } from "../connectors/ConnectorCard"
import ConnectorSelect from "./ConnectorSelect"

type ConnectorSelectTabProps = {
  opts: ElementOptions
  onSelect: (connector: Connector) => void
}

const ConnectorSelectTab: React.FC<ConnectorSelectTabProps> = ({
  opts,
  onSelect,
}) => (
  <>
    <WizardSubtitle title="Select a connector" />
    <ConnectorSelect onSelect={onSelect} />
    <WizardBottomBar
      opts={opts}
      actionText="Click on a connector to continue"
    />
  </>
)

export default ConnectorSelectTab
