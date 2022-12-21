import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import Loading from "components/layout/Loading"
// import MembershipMenu from "./MembershipMenu"

interface User {
  id: string
  username: string | null
}

interface Membership {
  id: string
  role: string
  user: User
  createdAt: string
}

type MembershipsTableProps = {
  memberships: Membership[]
  loading?: boolean
}

const MembershipsTable: React.FC<MembershipsTableProps> = ({
  memberships,
  loading,
}) => (
  <Table>
    <TableHead>
      <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
        <TableCell sx={{ pl: 1 }}>Name</TableCell>
        <TableCell>Role</TableCell>
        <TableCell>Created</TableCell>
        <TableCell sx={{ width: 0 }} />
      </TableRow>
    </TableHead>
    <TableBody>
      {memberships.map(membership => (
        <TableRow key={membership.id}>
          <TableCell sx={{ pl: 1 }}>{membership.user.username}</TableCell>
          <TableCell>{membership.role}</TableCell>
          <TableCell>{membership.createdAt}</TableCell>
          <TableCell sx={{ py: 0, px: 1 }}>
            {/* <MembershipMenu membership={key} /> */}
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
      {memberships.length === 0 && !loading && (
        <TableRow>
          <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
            <Typography>No Memberships</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default MembershipsTable
