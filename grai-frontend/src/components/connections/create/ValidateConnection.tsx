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

interface RunResult {
  id: string
  status: string
  metadata: any
}

type ValidateConnectionProps = {
  workspaceId: string
  run: Run
  onSuccess?: () => void
  onFail?: (run: RunResult) => void
  detailed?: boolean
}

const ValidateConnection: React.FC<ValidateConnectionProps> = ({
  workspaceId,
  run,
  onSuccess,
  onFail,
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
      onSuccess && onSuccess()
    }
    if (runError) {
      stopPolling()
      onFail && onFail(data.workspace.run)
    }

    return () => {
      stopPolling()
    }
  }, [success, runError, startPolling, stopPolling, onSuccess, onFail, data])

  if (error) return <GraphError error={error} />

  if (success) {
    return (
      <Alert severity="success">
        <AlertTitle>All tests successfully passed!</AlertTitle>
        {detailed ? "Continue to complete setting up your connection." : ""}
      </Alert>
    )
  }

  // if (runError)
  //   return (
  //     <Alert severity="error">
  //       <AlertTitle>
  //         Validation Failed
  //         {data.workspace.run.metadata.error !== "Unknown"
  //           ? ` - ${data.workspace.run.metadata.error}`
  //           : ""}
  //       </AlertTitle>
  //       {data.workspace.run.metadata.message}
  //       {data.workspace.run.metadata.error === "No connection" && (
  //         <Typography variant="body2" sx={{ mt: 1 }}>
  //           You may need to whitelist the Grai Cloud IP address, see{" "}
  //           <Link
  //             href="https://docs.grai.io/cloud/security/ip_whitelisting"
  //             target="_blank"
  //           >
  //             IP Whitelisting
  //           </Link>
  //         </Typography>
  //       )}
  //     </Alert>
  //   )

  return (
    <Alert severity="success" icon={<CircularProgress />}>
      <AlertTitle>Running tests</AlertTitle>
      Please wait while we validate your connection.
    </Alert>
  )
}

export default ValidateConnection
