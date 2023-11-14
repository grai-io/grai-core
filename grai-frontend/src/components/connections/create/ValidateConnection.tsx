import React, { useEffect } from "react"
import { gql, useQuery } from "@apollo/client"
import { Alert, AlertTitle, CircularProgress } from "@mui/material"
import GraphError from "components/utils/GraphError"
import {
  GetRunValidation,
  GetRunValidationVariables,
} from "./__generated__/GetRunValidation"

export const GET_RUN = gql`
  query GetRunValidation($workspaceId: ID!, $runId: ID!) {
    workspace(id: $workspaceId) {
      id
      run(id: $runId) {
        id
        status
        metadata
        connection {
          id
          validated
        }
      }
    }
  }
`

interface Run {
  id: string
}

type ValidateConnectionProps = {
  workspaceId: string
  run: Run
  onValidate?: () => void
  detailed?: boolean
}

const ValidateConnection: React.FC<ValidateConnectionProps> = ({
  workspaceId,
  run,
  onValidate,
  detailed,
}) => {
  const { error, data, startPolling, stopPolling } = useQuery<
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

    if (success) {
      stopPolling()
      onValidate && onValidate()
    }
    if (runError) stopPolling()

    return () => {
      stopPolling()
    }
  }, [success, runError, startPolling, stopPolling, onValidate])

  if (error) return <GraphError error={error} />

  if (success) {
    return (
      <Alert severity="success">
        <AlertTitle>All tests successfully passed!</AlertTitle>
        {detailed ? "Continue to complete setting up your connection." : ""}
      </Alert>
    )
  }

  if (runError)
    return (
      <Alert severity="error">
        <AlertTitle>
          Validation Failed
          {data.workspace.run.metadata.error !== "Unknown"
            ? ` - ${data.workspace.run.metadata.error}`
            : ""}
        </AlertTitle>
        {data.workspace.run.metadata.message}
      </Alert>
    )

  return (
    <Alert severity="success" icon={<CircularProgress />}>
      <AlertTitle>Running tests</AlertTitle>
      Please wait while we validate your connection.
    </Alert>
  )
}

export default ValidateConnection
