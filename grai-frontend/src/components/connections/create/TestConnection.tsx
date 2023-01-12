import { CheckCircle } from "@mui/icons-material"
import {
  Grid,
  Box,
  Typography,
  Divider,
  Alert,
  AlertTitle,
} from "@mui/material"
import React from "react"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Values } from "./CreateConnectionWizard"

type TestConnectionProps = {
  values: Values
}

const TestConnection: React.FC<TestConnectionProps> = ({ values }) => {
  return (
    <Grid container sx={{ mt: 5 }}>
      <Grid item md={8} sx={{ pr: 3 }}>
        <Box sx={{ display: "flex" }}>
          <CheckCircle color="success" />
          <Typography
            variant="body2"
            sx={{ ml: 2, color: theme => theme.palette.success.main }}
          >
            SUCCESS
          </Typography>
          <Typography variant="body2" sx={{ ml: 5 }}>
            Validate ability to access PostgreSQL
          </Typography>
        </Box>
        <Divider sx={{ mt: 2, mb: 3 }} />
        <Alert severity="success">
          <AlertTitle>All tests successfully passed!</AlertTitle>Continue to
          complete setting up your PostgreSQL connection.
        </Alert>
      </Grid>
      <Grid item md={4} sx={{}}>
        <CreateConnectionHelp connector={values.connector} />
      </Grid>
    </Grid>
  )
}

export default TestConnection
