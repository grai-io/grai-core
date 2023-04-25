import React, { useEffect } from "react"
import { gql, useQuery } from "@apollo/client"
import { CheckCircle, ArrowForward, Cancel } from "@mui/icons-material"
import {
  Grid,
  Box,
  Typography,
  Divider,
  Alert,
  AlertTitle,
  Button,
} from "@mui/material"
import Loading from "components/layout/Loading"
import GraphError from "components/utils/GraphError"
import WizardBottomBar from "components/wizards/WizardBottomBar"
import { ElementOptions } from "components/wizards/WizardLayout"
import {
  GetRunValidation,
  GetRunValidationVariables,
} from "./__generated__/GetRunValidation"
import CreateConnectionHelp from "./CreateConnectionHelp"
import { Connector } from "../connectors/ConnectorCard"

export const GET_RUN = gql`
  query GetRunValidation($workspaceId: ID!, $runId: ID!) {
    workspace(id: $workspaceId) {
      id
      run(id: $runId) {
        id
        status
        metadata
      }
    }
  }
`

interface Run {
  id: string
}

type ValidationRunProps = {
  workspaceId: string
  run: Run
  connector: Connector
  opts: ElementOptions
}

const ValidationRun: React.FC<ValidationRunProps> = ({
  workspaceId,
  run,
  connector,
  opts,
}) => {
  const { loading, error, data, startPolling, stopPolling } = useQuery<
    GetRunValidation,
    GetRunValidationVariables
  >(GET_RUN, {
    variables: {
      workspaceId,
      runId: run.id,
    },
  })

  const success = data?.workspace.run.status === "success"
  const runError = data?.workspace.run.status === "error"

  useEffect(() => {
    startPolling(1000)

    if (success) stopPolling()
    if (runError) stopPolling()

    return () => {
      stopPolling()
    }
  }, [success, runError, startPolling, stopPolling])

  if (error) return <GraphError error={error} />
  if (loading) return <Loading />

  if (success) {
    return (
      <>
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
                Validation Passed
              </Typography>
            </Box>
            <Divider sx={{ mt: 2, mb: 3 }} />
            <Alert severity="success">
              <AlertTitle>All tests successfully passed!</AlertTitle>Continue to
              complete setting up your connection.
            </Alert>
          </Grid>
          <Grid item md={4} sx={{}}>
            <CreateConnectionHelp connector={connector} />
          </Grid>
        </Grid>
        <WizardBottomBar opts={opts}>
          <Button
            variant="contained"
            type="submit"
            sx={{ minWidth: 120 }}
            endIcon={<ArrowForward />}
            onClick={opts.forwardStep}
          >
            Continue
          </Button>
        </WizardBottomBar>
      </>
    )
  }

  return (
    <>
      <Grid container sx={{ mt: 5 }}>
        <Grid item md={8} sx={{ pr: 3 }}>
          {runError ? (
            <>
              <Box sx={{ display: "flex" }}>
                <Cancel color="error" />
                <Typography
                  variant="body2"
                  sx={{ ml: 2, color: theme => theme.palette.error.main }}
                >
                  ERROR
                </Typography>
                <Typography variant="body2" sx={{ ml: 5 }}>
                  Validation Failed
                </Typography>
              </Box>
              <Divider sx={{ mt: 2, mb: 3 }} />
              <Alert severity="error">
                <AlertTitle>Validation log</AlertTitle>
                {data.workspace.run.metadata.error}
              </Alert>
            </>
          ) : (
            <Box sx={{ display: "flex" }}>
              <CheckCircle color="success" />
              <Typography
                variant="body2"
                sx={{ ml: 2, color: theme => theme.palette.success.main }}
              >
                RUNNING
              </Typography>
              <Typography variant="body2" sx={{ ml: 5 }}>
                Validating connection
              </Typography>
            </Box>
          )}
        </Grid>
        <Grid item md={4} sx={{}}>
          <CreateConnectionHelp connector={connector} />
        </Grid>
      </Grid>
      <WizardBottomBar opts={opts}>
        <Button
          variant="contained"
          type="submit"
          sx={{ minWidth: 120 }}
          endIcon={<ArrowForward />}
          disabled
        >
          Continue
        </Button>
      </WizardBottomBar>
    </>
  )
}

export default ValidationRun
