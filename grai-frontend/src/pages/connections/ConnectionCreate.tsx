import { Grid, Typography } from "@mui/material"
import React from "react"
import CreateConnectionForm from "components/connections/CreateConnectionForm"
import PageLayout from "components/layout/PageLayout"

const ConnectionCreate: React.FC = () => (
  <PageLayout padding>
    <Typography variant="h4">Create Connection</Typography>
    <Grid container>
      <Grid item md={4}>
        <CreateConnectionForm />
      </Grid>
    </Grid>
  </PageLayout>
)

export default ConnectionCreate
