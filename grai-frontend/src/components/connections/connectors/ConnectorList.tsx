import React from "react"
import { Grid } from "@mui/material"
import ConnectorCard, { Connector } from "./ConnectorCard"

type ConnectorListProps = {
  connectors: Connector[]
  onSelect: (connector: Connector) => void
}

const ConnectorList: React.FC<ConnectorListProps> = ({
  connectors,
  onSelect,
}) => (
  <Grid container spacing={2}>
    {connectors.map(connector => (
      <Grid item md={3} key={connector.id}>
        <ConnectorCard connector={connector} onSelect={onSelect} />
      </Grid>
    ))}
  </Grid>
)

export default ConnectorList
