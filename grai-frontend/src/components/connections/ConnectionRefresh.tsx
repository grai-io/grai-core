import { gql, useMutation } from "@apollo/client"
import { Refresh } from "@mui/icons-material"
import { LoadingButton } from "@mui/lab"
import {
  MenuItem,
  ListItemIcon,
  ListItemText,
  CircularProgress,
} from "@mui/material"
import React from "react"
import {
  RunConnection,
  RunConnectionVariables,
} from "./__generated__/RunConnection"

export const RUN_CONNECTION = gql`
  mutation RunConnection($connectionId: ID!) {
    runConnection(connectionId: $connectionId) {
      id
      status
      created_at
      started_at
      finished_at
      user {
        id
        first_name
      }
    }
  }
`

interface Run {
  id: string
  status: string
}

interface Connection {
  id: string
  last_run: Run | null
}

type ConnectionRefreshProps = {
  connection: Connection
  menuItem?: boolean
  disabled?: boolean
}

const ConnectionRefresh: React.FC<ConnectionRefreshProps> = ({
  connection,
  menuItem,
  disabled,
}) => {
  const [runConnection, { loading }] = useMutation<
    RunConnection,
    RunConnectionVariables
  >(RUN_CONNECTION, {
    variables: {
      connectionId: connection.id,
    },
  })

  const handleClick = () => runConnection()

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
