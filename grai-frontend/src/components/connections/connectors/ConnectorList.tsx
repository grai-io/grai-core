import React from "react"
import { Typography, Grid } from "@mui/material"
import ConnectorCard, { Connector } from "./ConnectorCard"

type ConnectorListProps = {
  title: string
  connectors: Connector[]
  onSelect: (connector: Connector) => void
}

const ConnectorList: React.FC<ConnectorListProps> = ({
  title,
  connectors,
  onSelect,
}) => (
  <>
    <Typography variant="h6" sx={{ mt: 5, mb: 3, textTransform: "capitalize" }}>
      {title}
    </Typography>
    <Grid container spacing={2}>
      {connectors.map(connector => (
        <Grid item md={3} key={connector.id}>
          <ConnectorCard connector={connector} onSelect={onSelect} />
        </Grid>
      ))}
    </Grid>
  </>
)

export default ConnectorList
