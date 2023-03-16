import React from "react"
import { gql, useMutation } from "@apollo/client"
import { PlayArrow } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material"
import { clearWorkspace } from "helpers/cache"
import { DateTime } from "luxon"
import {
  RunConnection,
  RunConnectionVariables,
} from "./__generated__/RunConnection"

export const RUN_CONNECTION = gql`
  mutation RunConnection($connectionId: ID!) {
    runConnection(connectionId: $connectionId) {
      id
      connection {
        id
        last_run {
          id
          status
          created_at
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
        }
        last_successful_run {
          id
          status
          started_at
          finished_at
          metadata
          user {
            id
            first_name
            last_name
          }
        }
        runs {
          id
          status
          created_at
          started_at
          finished_at
          user {
            id
            first_name
            last_name
          }
          metadata
        }
      }
    }
  }
`

interface User {
  id: string
  first_name: string
  last_name: string
}

interface Run {
  id: string
  status: string
  created_at: string
  started_at: string | null
  finished_at: string | null
  user: User | null
  metadata: any
}

export interface Connection {
  id: string
  name: string
  last_run: Run | null
  last_successful_run: Run | null
  runs: Run[]
}

export interface RunResult {
  id: string
}

type ConnectionRunProps = {
  connection: Connection
  workspaceId: string
  menuItem?: boolean
  disabled?: boolean
  onRun?: (run: RunResult) => void
}

const ConnectionRun: React.FC<ConnectionRunProps> = ({
  connection,
  workspaceId,
  menuItem,
  disabled,
  onRun,
}) => {
  const runToTypedRun = (run: Run) => ({
    ...run,
    user: run.user ? { ...run.user, __typename: "User" as const } : null,
    __typename: "Run" as const,
  })

  const [runConnection, { loading }] = useMutation<
    RunConnection,
    RunConnectionVariables
  >(RUN_CONNECTION, {
    variables: {
      connectionId: connection.id,
    },
    update(cache) {
      clearWorkspace(cache, workspaceId)
    },
  })

  const tmpRun = {
    id: "tmp-id",
    __typename: "Run" as const,
    status: "queued",
    created_at: DateTime.now(),
    started_at: null,
    finished_at: null,
    metadata: {},
    user: null,
  }

  const handleClick = () =>
    runConnection({
      optimisticResponse: {
        runConnection: {
          id: "temp",
          connection: {
            id: connection.id,
            __typename: "Connection",
            runs: [tmpRun, ...connection.runs.map(runToTypedRun)],
            last_successful_run: connection.last_successful_run
              ? runToTypedRun(connection.last_successful_run)
              : null,
            last_run: tmpRun,
          },
          __typename: "Run",
        },
      },
    }).then(
      data =>
        onRun &&
        data.data?.runConnection.connection.last_run &&
        onRun(data.data.runConnection.connection.last_run)
    )

  const loading2 =
    loading ||
    (connection.last_run?.status
      ? ["queued", "running"].includes(connection.last_run.status)
      : false)

  if (menuItem)
    return (
      <MenuItem disabled={disabled || loading} onClick={handleClick}>
        <ListItemIcon>
          {loading2 ? <CircularProgress /> : <PlayArrow />}
        </ListItemIcon>
        <ListItemText primary="Run" />
      </MenuItem>
    )

  return (
    <LoadingButton
      onClick={handleClick}
      variant="outlined"
      startIcon={<PlayArrow />}
      disabled={disabled}
      loading={loading2}
      loadingPosition="start"
      data-testid="connection-run"
    >
      {(loading2 && connection.last_run?.status) || "Run"}
    </LoadingButton>
  )
}

export default ConnectionRun
