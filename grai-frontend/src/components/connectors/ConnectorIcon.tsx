import React from "react"
import { Box, Tooltip } from "@mui/material"

interface Connector {
  name: string
  icon: string | null
}

type ConnectorIconProps = {
  connector: Connector
  noBorder?: boolean
}

const ConnectorIcon: React.FC<ConnectorIconProps> = ({ connector, noBorder }) =>
  connector.icon ? (
    <Tooltip title={connector.name}>
      <Box
        sx={{
          borderRadius: "8px",
          border: noBorder ? null : "1px solid rgba(0, 0, 0, 0.08)",
          height: "48px",
          width: "48px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <img
          src={connector.icon}
          alt={`${connector.name} logo`}
          style={{ height: 32, width: 32 }}
        />
      </Box>
    </Tooltip>
  ) : null

export default ConnectorIcon
