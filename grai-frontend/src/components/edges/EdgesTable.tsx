import {
  CircularProgress,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material"
import React from "react"
import { Edge } from "../../pages/edges/Edges"

type EdgesTableProps = {
  edges: Edge[] | null
}

const EdgesTable: React.FC<EdgesTableProps> = ({ edges }) => (
  <Table size="small">
    <TableHead>
      <TableRow>
        <TableCell>id</TableCell>
        <TableCell>Data Source</TableCell>
        <TableCell>Source</TableCell>
        <TableCell>Destination</TableCell>
        <TableCell>Active</TableCell>
      </TableRow>
    </TableHead>
    <TableBody>
      {edges?.map(edge => (
        <TableRow key={edge.id}>
          <TableCell>{edge.id}</TableCell>
          <TableCell>{edge.dataSource}</TableCell>
          <TableCell>{edge.source.displayName ?? edge.source.name}</TableCell>
          <TableCell>
            {edge.destination.displayName ?? edge.destination.name}
          </TableCell>
          <TableCell>{edge.isActive ? "Yes" : "No"}</TableCell>
        </TableRow>
      ))}
      {!edges && (
        <TableRow>
          <TableCell colSpan={99}>
            <CircularProgress />
          </TableCell>
        </TableRow>
      )}
    </TableBody>
  </Table>
)

export default EdgesTable
