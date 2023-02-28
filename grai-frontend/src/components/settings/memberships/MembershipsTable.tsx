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
// import MembershipMenu from "./MembershipMenu"

interface User {
  id: string
  username: string | null
  first_name: string
  last_name: string
}

interface Membership {
  id: string
  role: string
  user: User
  is_active: boolean
  created_at: string
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
        <TableCell>Email</TableCell>
        <TableCell>Name</TableCell>
        <TableCell>Role</TableCell>
        <TableCell>Active</TableCell>
        <TableCell sx={{ width: 300 }}>Created</TableCell>
        <TableCell sx={{ width: 0 }} />
      </TableRow>
    </TableHead>
    <TableBody>
      {memberships.map(membership => (
        <TableRow key={membership.id}>
          <TableCell>{membership.user.username}</TableCell>
          <TableCell>
            {membership.user.first_name} {membership.user.last_name}
          </TableCell>
          <TableCell>{membership.role}</TableCell>
          <TableCell>{membership.is_active ? "Yes" : "No"}</TableCell>
          <TableCell>{membership.created_at}</TableCell>
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
            <Typography>No memberships found</Typography>
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default MembershipsTable
