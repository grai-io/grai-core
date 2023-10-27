import React from "react"
import {
  Table,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"
import DataSourcesStack, { Source } from "components/tables/DataSourcesStack"
import TableCell from "components/tables/TableCell"
import TagsStack from "components/tables/TagsStack"

interface SourceNode {
  id: string
  namespace: string
  name: string
  display_name: string
  is_active: boolean
  metadata: any
  data_sources: { data: Source[] }
}

type SourceNodesTableProps = {
  nodes: SourceNode[]
  loading?: boolean
  total: number
  page: number
  onPageChange: (page: number) => void
}

const SourceNodesTable: React.FC<SourceNodesTableProps> = ({
  nodes,
  loading,
  total,
  page,
  onPageChange,
}) => {
  const navigate = useNavigate()
  const { routePrefix } = useWorkspace()

  return (
    <Table>
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
            onClick={() => navigate(`${routePrefix}/nodes/${node.id}`)}
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
              <TagsStack tags={node.metadata?.grai?.tags} />
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
        {!loading && nodes.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ py: 10, textAlign: "center" }}>
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
          onPageChange={onPageChange}
          type="nodes"
        />
      </TableFooter>
    </Table>
  )
}

export default SourceNodesTable
