import React from "react"
import {
  Table,
  TableBody,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import { DateTime } from "luxon"
import Loading from "components/layout/Loading"
import TableCell from "components/tables/TableCell"
import AlertMenu from "./AlertMenu"

interface Alert {
  id: string
  name: string
  channel: string
  is_active: boolean
  created_at: string
}

type AlertsTableProps = {
  alerts: Alert[]
  loading?: boolean
  workspaceId?: string
}

const AlertsTable: React.FC<AlertsTableProps> = ({
  alerts,
  loading,
  workspaceId,
}) => {
  const { workspaceNavigate } = useWorkspace()

  const handleRowClick = (alert: Alert) => () =>
    workspaceNavigate(`settings/alerts/${alert.id}`)

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>Name</TableCell>
          <TableCell>Channel</TableCell>
          <TableCell>Active</TableCell>
          <TableCell sx={{ width: 300 }}>Created</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {alerts.map(alert => (
          <TableRow
            key={alert.id}
            onClick={handleRowClick(alert)}
            hover
            sx={{ cursor: "pointer" }}
          >
            <TableCell>{alert.name}</TableCell>
            <TableCell>{alert.channel}</TableCell>
            <TableCell>{alert.is_active ? "Yes" : "No"}</TableCell>
            <TableCell>
              {DateTime.fromISO(alert.created_at).toLocaleString(
                DateTime.DATETIME_MED
              )}
            </TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              <AlertMenu alert={alert} workspaceId={workspaceId} />
            </TableCell>
          </TableRow>
        ))}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
        {alerts.length === 0 && !loading && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No alerts found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default AlertsTable
