import {
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import Loading from "../../layout/Loading"
import ApiKeyMenu from "./ApiKeyMenu"

interface User {
  id: string
  username: string | null
}

interface Key {
  id: string
  name: string
  prefix: string
  created: string
  revoked: boolean
  expiryDate: string
  createdBy: User
}

type ApiKeysTableProps = {
  keys: Key[]
  loading?: boolean
}

const ApiKeysTable: React.FC<ApiKeysTableProps> = ({ keys, loading }) => (
  <Table>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell sx={{ width: 0, p: 0 }}>
          <Checkbox size="small" />
        </TableCell>

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
          <TableCell sx={{ p: 0 }}>
            <Checkbox size="small" />
          </TableCell>

          <TableCell sx={{ pl: 1 }}>{key.name}</TableCell>
          <TableCell>{key.prefix}***********</TableCell>
          <TableCell>{key.created}</TableCell>
          <TableCell>{key.createdBy.username}</TableCell>
          <TableCell>{key.expiryDate}</TableCell>
          <TableCell>{key.revoked ? "Yes" : ""}</TableCell>
          <TableCell sx={{ py: 0, px: 1 }}>
            <ApiKeyMenu apiKey={key} />
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
            <Typography>No API keys</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default ApiKeysTable
