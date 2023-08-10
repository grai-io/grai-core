import React from "react"
import {
  Chip,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"
import DataSourcesStack, { Source } from "components/tables/DataSourcesStack"

interface Node {
  id: string
  namespace: string
  name: string
  display_name: string
  is_active: boolean
  metadata: any
  data_sources: { data: Source[] }
}

type NodesTableProps = {
  nodes: Node[]
  loading?: boolean
  total: number
  page: number
  onPageChange: (page: number) => void
}

const NodesTable: React.FC<NodesTableProps> = ({
  nodes,
  loading,
  total,
  page,
  onPageChange,
}) => {
  const navigate = useNavigate()

  return (
    <Table sx={{ mb: -1 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell>Namespace</TableCell>
          <TableCell>Node Type</TableCell>
          <TableCell>Data Sources</TableCell>
          <TableCell>Active</TableCell>
          <TableCell>Tags</TableCell>
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
            <TableCell>{node.display_name ?? node.name}</TableCell>
            <TableCell>{node.namespace}</TableCell>
            <TableCell>{node.metadata?.grai?.node_type}</TableCell>
            <TableCell sx={{ py: 0, pl: 1 }}>
              <DataSourcesStack data_sources={node.data_sources} />
            </TableCell>
            <TableCell>{node.is_active ? "Yes" : "No"}</TableCell>
            <TableCell sx={{ py: 0 }}>
              <Stack direction="row" spacing={1}>
                {node.metadata?.grai?.tags?.map((tag: string) => (
                  <Chip label={tag} key={tag} />
                ))}
              </Stack>
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
        {nodes.length === 0 && !loading && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No nodes found</Typography>
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={20}
          page={page}
          type="tables"
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>
  )
}

export default NodesTable
