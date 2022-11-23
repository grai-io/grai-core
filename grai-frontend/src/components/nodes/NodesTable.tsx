import {
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import { Node } from "../../pages/nodes/Nodes"

type NodesTableProps = {
  nodes: Node[] | null
}

const NodesTable: React.FC<NodesTableProps> = ({ nodes }) => {
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
        {nodes?.map(node => (
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
            <TableCell>{node.display_name}</TableCell>
            <TableCell>{node.namespace}</TableCell>
            <TableCell>{node.data_source}</TableCell>
            <TableCell>{node.is_active ? "Yes" : "No"}</TableCell>
          </TableRow>
        ))}
        {!nodes && (
          <TableRow>
            <TableCell colSpan={99}>
              <CircularProgress />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  )
}

export default NodesTable
