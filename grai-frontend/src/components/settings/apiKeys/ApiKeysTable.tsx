import React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { DateTime } from "luxon"
import Loading from "components/layout/Loading"
import ApiKeyMenu from "./ApiKeyMenu"

interface User {
  id: string
  username: string | null
  first_name: string | null
  last_name: string | null
}

interface Key {
  id: string
  name: string
  prefix: string
  created: string
  revoked: boolean
  expiry_date: string | null
  created_by: User
}

type ApiKeysTableProps = {
  keys: Key[]
  loading?: boolean
  workspaceId?: string
}

const ApiKeysTable: React.FC<ApiKeysTableProps> = ({
  keys,
  loading,
  workspaceId,
}) => (
  <Table>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell sx={{ pl: 1 }}>Name</TableCell>
        <TableCell>Key</TableCell>
        <TableCell>Created</TableCell>
        <TableCell>Created by</TableCell>
        <TableCell>Expires</TableCell>
        <TableCell>Revoked</TableCell>
        <TableCell sx={{ width: 0 }} />
      </TableRow>
    </TableHead>
    <TableBody>
      {keys.map(key => (
        <TableRow key={key.id}>
          <TableCell sx={{ pl: 1 }}>{key.name}</TableCell>
          <TableCell>{key.prefix}***********</TableCell>
          <TableCell>
            {DateTime.fromISO(key.created).toLocaleString(DateTime.DATE_MED)}
          </TableCell>
          <TableCell>
            {key.created_by.first_name
              ? `${key.created_by.first_name} ${key.created_by.last_name}`
              : key.created_by.username}
          </TableCell>
          <TableCell>
            {key.expiry_date &&
              DateTime.fromISO(key.expiry_date).toLocaleString(
                DateTime.DATE_MED
              )}
          </TableCell>
          <TableCell>{key.revoked ? "Yes" : ""}</TableCell>
          <TableCell sx={{ py: 0, px: 1 }}>
            <ApiKeyMenu apiKey={key} workspaceId={workspaceId} />
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
      {keys.length === 0 && !loading && (
        <TableRow>
          <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
            <Typography>No API keys found</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default ApiKeysTable
