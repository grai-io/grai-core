import React from "react"
import { Box, Typography } from "@mui/material"
import { ElementOptions } from "components/wizards/WizardLayout"
import ConnectorSelect from "./ConnectorSelect"
import { Connector } from "../connectors/ConnectorCard"

type ConnectorSelectTabProps = {
  opts: ElementOptions
  onSelect: (connector: Connector) => void
}

const ConnectorSelectTab: React.FC<ConnectorSelectTabProps> = ({
  onSelect,
}) => (
  <>
    <Box>
      <Typography
        variant="h6"
        sx={{
          color: "#1F2A37",
          fontSize: 22,
          fontWeight: 800,
          lineHeight: "150%",
          letterSpacing: "0.22px",
          mb: "14px",
        }}
      >
        Select integration
      </Typography>
      <Typography>Choose the integration for your workflow</Typography>
    </Box>
    <ConnectorSelect onSelect={onSelect} />
  </>
)

export default ConnectorSelectTab
