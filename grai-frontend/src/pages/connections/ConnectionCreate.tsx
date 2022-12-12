import { Box, Grid, Typography } from "@mui/material"
import React from "react"
import ConnectionsForm from "../../components/connections/ConnectionsForm"
import AppTopBar from "../../components/layout/AppTopBar"

const ConnectionCreate: React.FC = () => (
  <>
    <AppTopBar />
    <Box sx={{ p: 3 }}>
      <Typography variant="h4">Create Connection</Typography>
      <Grid container>
        <Grid item md={4}>
          <ConnectionsForm />
        </Grid>
      </Grid>
    </Box>
  </>
)

export default ConnectionCreate
