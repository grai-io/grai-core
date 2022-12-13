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
    <Table size="small">
      <TableHead>
        <TableRow>
          <TableCell>id</TableCell>
          <TableCell>Name</TableCell>
          <TableCell>Display Name</TableCell>
          <TableCell> Namespace</TableCell>
          <TableCell>Data Source</TableCell>
          <TableCell>Active</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {nodes.map(node => (
          <TableRow
            key={node.id}
            onClick={() => navigate(`/nodes/${node.id}`)}
            hover
            sx={{
              cursor: "pointer",
            }}
          >
            <TableCell>{node.id}</TableCell>
            <TableCell>{node.name}</TableCell>
            <TableCell>{node.displayName}</TableCell>
            <TableCell>{node.namespace}</TableCell>
            <TableCell>{node.dataSource}</TableCell>
            <TableCell>{node.isActive ? "Yes" : "No"}</TableCell>
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
