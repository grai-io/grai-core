import React from "react"
import { Box, Toolbar, Typography } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import ConnectionToolbar from "./ConnectionToolbar"
import { Connector } from "../connectors/ConnectorCard"
import ConnectorIcon from "../connectors/ConnectorIcon"

type ConnectorToolbarProps = {
  connector: Connector
}

const ConnectorToolbar: React.FC<ConnectorToolbarProps> = ({ connector }) => {
  const { routePrefix } = useWorkspace()

  return (
    <PageContent noPadding>
      <ConnectionToolbar
        title="Setup Connection"
        activeStep={1}
        onBack={`${routePrefix}/connections/create`}
      />
      <Toolbar
        sx={{
          p: 3,
          display: "flex",
          alignItems: "center",
          borderRadius: "0px 0px 12px 12px",
          background: "linear-gradient(243deg, #F7F4FE 0%, #F3F7FF 100%)",
        }}
      >
        <Box
          sx={{
            width: "48px",
            height: "48px",
            backgroundColor: "#F8F8F8",
            borderRadius: "24px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <ConnectorIcon connector={connector} />
        </Box>
        <Typography
          sx={{
            color: "#1F2A37",
            fontSize: "20px",
            fontWeight: 800,
            ml: 2,
          }}
        >
          Connect to {connector.name}
        </Typography>
      </Toolbar>
    </PageContent>
  )
}

export default ConnectorToolbar
