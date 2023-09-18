import React from "react"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import Loading from "components/layout/Loading"
// import ApiKeyMenu from "./ApiKeyMenu"

interface Key {
  id: string
  name: string
}

type TwoFactorTableProps = {
  keys: Key[]
  loading?: boolean
}

const TwoFactorTable: React.FC<TwoFactorTableProps> = ({ keys, loading }) => (
  <Table>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell sx={{ pl: 1 }}>Name</TableCell>
        <TableCell sx={{ width: 0 }} />
      </TableRow>
    </TableHead>
    <TableBody>
      {keys.map(key => (
        <TableRow key={key.id}>
          <TableCell sx={{ pl: 1 }}>{key.name}</TableCell>
          <TableCell />
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
            <Typography>No 2FA keys found</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default TwoFactorTable
