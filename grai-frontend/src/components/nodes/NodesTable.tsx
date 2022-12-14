import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import { Node } from "../../pages/nodes/Nodes"
import Loading from "../layout/Loading"

type NodesTableProps = {
  nodes: Node[]
  loading?: boolean
}

const NodesTable: React.FC<NodesTableProps> = ({ nodes, loading }) => {
  const navigate = useNavigate()

  return (
    <Table>
      <TableHead>
        <TableRow sx={{ backgroundColor: theme => theme.palette.grey[100] }}>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Data Source</TableCell>
          <TableCell>Active</TableCell>
          <TableCell>Last updated</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {nodes.map(node => (
          <TableRow
            key={node.id}
            onClick={() => navigate(node.id)}
            hover
            sx={{
              cursor: "pointer",
            }}
          >
            <TableCell>{node.displayName ?? node.name}</TableCell>
            <TableCell>{node.namespace}</TableCell>
            <TableCell>{node.dataSource}</TableCell>
            <TableCell>{node.isActive ? "Yes" : "No"}</TableCell>
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
        {!nodes && !loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Typography>No nodes found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default NodesTable
