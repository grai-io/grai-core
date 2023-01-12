import { Grid } from "@mui/material"
import React from "react"
import CreateConnectionHelp from "../create/CreateConnectionHelp"
import UpdateConnectionForm, { Connection } from "./UpdateConnectionForm"

type ConnectionConfigurationProps = {
  connection: Connection
}

const ConnectionConfiguration: React.FC<ConnectionConfigurationProps> = ({
  connection,
}) => (
  <Grid container sx={{ mt: 5 }}>
    <Grid item md={8} sx={{ pr: 3 }}>
      <UpdateConnectionForm connection={connection} />
    </Grid>
    <Grid item md={4} sx={{}}>
      <CreateConnectionHelp connector={connection.connector} />
    </Grid>
  </Grid>
)

export default ConnectionConfiguration
