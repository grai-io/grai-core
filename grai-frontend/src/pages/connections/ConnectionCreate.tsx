import { Box, Grid, Typography } from "@mui/material"
import React from "react"
import CreateConnectionForm from "../../components/connections/CreateConnectionForm"
import AppTopBar from "../../components/layout/AppTopBar"

const ConnectionCreate: React.FC = () => (
  <>
    <AppTopBar />
    <Box sx={{ p: 3 }}>
      <Typography variant="h4">Create Connection</Typography>
      <Grid container>
        <Grid item md={4}>
          <CreateConnectionForm />
        </Grid>
      </Grid>
    </Box>
  </>
)

export default ConnectionCreate
