import React from "react"
import {
  Box,
  Chip,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableFooter,
  TableHead,
  TableRow,
  TableSortLabel,
  Typography,
} from "@mui/material"
import { visuallyHidden } from "@mui/utils"
import { useNavigate } from "react-router-dom"
import { Order } from "pages/nodes/Nodes"
import Loading from "components/layout/Loading"
import TablePagination from "components/table/TablePagination"
import DataSourcesStack, { Source } from "components/tables/DataSourcesStack"

type TableHeadCellProps = {
  property: string
  title?: string
  noOrder?: boolean
}

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
  order: Order | null
  onOrderChange: (order: Order) => void
}

const NodesTable: React.FC<NodesTableProps> = ({
  nodes,
  loading,
  total,
  page,
  onPageChange,
  order,
  onOrderChange,
}) => {
  const navigate = useNavigate()

  const handleSort = (property: string) => () =>
    onOrderChange({
      property,
      direction:
        order?.property === property && order.direction === "asc"
          ? "desc"
          : "asc",
    })

  const TableHeadCell: React.FC<TableHeadCellProps> = ({
    property,
    title,
    noOrder,
  }) =>
    noOrder ? (
      <TableCell>{title ?? property}</TableCell>
    ) : (
      <TableCell>
        <TableSortLabel
          active={order?.property === property}
          direction={order?.property === property ? order.direction : "asc"}
          onClick={handleSort(property)}
        >
          {title ?? property}
          {order?.property === property ? (
            <Box component="span" sx={visuallyHidden}>
              {order?.direction === "desc"
                ? "sorted descending"
                : "sorted ascending"}
            </Box>
          ) : null}
        </TableSortLabel>
      </TableCell>
    )

  return (
    <Table sx={{ mb: -1 }}>
      <TableHead>
        <TableRow>
          <TableHeadCell property="name" title="Name" />
          <TableHeadCell property="namespace" title="Namespace" />
          <TableHeadCell
            property="metadata__grai__node_type"
            title="Node Type"
          />
          <TableHeadCell property="data_sources" title="Data Sources" noOrder />
          <TableHeadCell property="is_active" title="Active" />
          <TableHeadCell property="tags" title="Tags" noOrder />
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
          type="nodes"
          onPageChange={onPageChange}
        />
      </TableFooter>
    </Table>
  )
}

export default NodesTable
