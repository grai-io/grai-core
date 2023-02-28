import React from "react"
import { ArrowForward, CheckCircle } from "@mui/icons-material"
import {
  Grid,
  Box,
  Typography,
  Divider,
  Alert,
  AlertTitle,
  Button,
} from "@mui/material"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import WizardSubtitle from "components/wizards/WizardSubtitle"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Values } from "./CreateConnectionWizard"

type TestConnectionProps = {
  opts: ElementOptions
  values: Values
}

const TestConnection: React.FC<TestConnectionProps> = ({ opts, values }) => {
  return (
    <>
      <WizardSubtitle
        title={`Test connection to ${values.connector?.name}`}
        icon={values.connector?.icon}
      />
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
      <WizardBottomBar opts={opts}>
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120, color: "white" }}
          endIcon={<ArrowForward />}
          onClick={opts.forwardStep}
        >
          Continue
        </Button>
      </WizardBottomBar>
    </>
  )
}

export default TestConnection
