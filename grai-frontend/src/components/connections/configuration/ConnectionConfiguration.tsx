import React from "react"
import { Grid } from "@mui/material"
import UpdateConnectionForm, {
  Connection,
  Workspace,
} from "./UpdateConnectionForm"
import CreateConnectionHelp from "../create/CreateConnectionHelp"

type ConnectionConfigurationProps = {
  connection: Connection
  workspace: Workspace
}

const ConnectionConfiguration: React.FC<ConnectionConfigurationProps> = ({
  connection,
  workspace,
}) => (
  <Grid container>
    <Grid item md={8} sx={{ pr: 3 }}>
      <UpdateConnectionForm connection={connection} workspace={workspace} />
    </Grid>
    <Grid item md={4} sx={{}}>
      <CreateConnectionHelp connector={connection.connector} />
    </Grid>
  </Grid>
)

export default ConnectionConfiguration
