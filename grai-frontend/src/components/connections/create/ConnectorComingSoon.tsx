import React from "react"
import { Card, Typography } from "@mui/material"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import { ConnectorType } from "../ConnectionsForm"

type ConnectorComingSoonProps = {
  connector: ConnectorType
  opts: ElementOptions
}

const ConnectorComingSoon: React.FC<ConnectorComingSoonProps> = ({
  connector,
  opts,
}) => (
  <>
    <WizardSubtitle
      title={`${connector?.name} Integration`}
      icon={connector?.icon}
    />

    <Card
      elevation={0}
      variant="outlined"
      sx={{ textAlign: "center", mt: 10, py: 10, borderRadius: "20px" }}
    >
      <Typography variant="h5">{connector.name} coming soon</Typography>
      <Typography sx={{ mt: 5, lineHeight: "2rem" }}>
        We would love to build this integration for you,
        <br />
        just get in touch on Slack.
      </Typography>
    </Card>
    <WizardBottomBar opts={opts} />
  </>
)

export default ConnectorComingSoon
