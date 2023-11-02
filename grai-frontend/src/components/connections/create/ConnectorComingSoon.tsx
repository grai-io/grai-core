import React from "react"
import { Box, Button, Typography } from "@mui/material"
import { ElementOptions } from "components/wizards/WizardLayout"
import { ConnectorType } from "../ConnectionsForm"

type ConnectorComingSoonProps = {
  connector: ConnectorType
  opts: ElementOptions
}

const ConnectorComingSoon: React.FC<ConnectorComingSoonProps> = ({
  connector,
  opts,
}) => (
  <Box sx={{ textAlign: "center", pt: 5, pb: 10, borderRadius: "20px" }}>
    <Typography variant="h5">{connector.name} coming soon</Typography>
    <Typography sx={{ mt: 5, lineHeight: "2rem", mb: 10 }}>
      We would love to build this integration for you,
      <br />
      just get in touch on Slack.
    </Typography>
    <Button variant="outlined" onClick={opts.backStep}>
      Go Back
    </Button>
  </Box>
)

export default ConnectorComingSoon
