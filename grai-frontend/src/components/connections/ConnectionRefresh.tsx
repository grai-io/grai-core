import { gql, useMutation } from "@apollo/client"
import { Refresh } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material"
import { DateTime } from "luxon"
import React from "react"
import {
  RunConnection,
  RunConnectionVariables,
} from "./__generated__/RunConnection"

export const RUN_CONNECTION = gql`
  mutation RunConnection($connectionId: ID!) {
    runConnection(connectionId: $connectionId) {
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
  last_run: Run | null
  last_successful_run: Run | null
  runs: Run[]
}

type ConnectionRefreshProps = {
  connection: Connection
  menuItem?: boolean
  disabled?: boolean
  onRefresh?: () => void
}

const ConnectionRefresh: React.FC<ConnectionRefreshProps> = ({
  connection,
  menuItem,
  disabled,
  onRefresh,
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
          id: connection.id,
          __typename: "Connection",
          runs: [tmpRun, ...connection.runs.map(runToTypedRun)],
          last_successful_run: connection.last_successful_run
            ? runToTypedRun(connection.last_successful_run)
            : null,
          last_run: tmpRun,
        },
      },
    }).then(() => onRefresh && onRefresh())

  const loading2 =
    loading ||
    (connection.last_run?.status
      ? ["queued", "running"].includes(connection.last_run.status)
      : false)

  if (menuItem)
    return (
      <MenuItem disabled={disabled || loading} onClick={handleClick}>
        <ListItemIcon>
          {loading2 ? <CircularProgress /> : <Refresh />}
        </ListItemIcon>
        <ListItemText primary="Refresh" />
      </MenuItem>
    )

  return (
    <LoadingButton
      onClick={handleClick}
      variant="outlined"
      startIcon={<Refresh />}
      disabled={disabled}
      loading={loading2}
      loadingPosition="start"
      data-testid="connection-refresh"
    >
      {(loading2 && connection.last_run?.status) || "Refresh"}
    </LoadingButton>
  )
}

export default ConnectionRefresh
