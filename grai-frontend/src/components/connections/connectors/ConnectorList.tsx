import React from "react"
import { Grid } from "@mui/material"
import ConnectorCard, { Connector } from "./ConnectorCard"

type ConnectorListProps = {
  connectors: Connector[]
}

const ConnectorList: React.FC<ConnectorListProps> = ({ connectors }) => (
  <Grid container spacing={2}>
    {connectors.map(connector => (
      <Grid item md={3} key={connector.id}>
        <ConnectorCard connector={connector} />
      </Grid>
    ))}
  </Grid>
)

export default ConnectorList
