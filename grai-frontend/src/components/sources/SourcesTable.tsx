import React from "react"
import {
  Card,
  CardActionArea,
  Table,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { Link, useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ConnectorIcon from "components/connectors/ConnectorIcon"
import Loading from "components/layout/Loading"
import RunStatus from "components/runs/RunStatus"
import TablePagination from "components/table/TablePagination"
import TableCell from "components/tables/TableCell"
import SourcesMenu from "./SourcesMenu"

interface Connector {
  id: string
  name: string
  icon: string | null
  // events: boolean
}

interface Run {
  id: string
  status: string
}

interface Connection {
  id: string
  name: string
  connector: Connector
  last_run: Run | null
}

interface Source {
  id: string
  name: string
  nodes: {
    meta: {
      total: number
    }
  }
  edges: {
    meta: {
      total: number
    }
  }
  connections: {
    data: Connection[]
  }
}

type SourcesTableProps = {
  sources: Source[]
  workspaceId: string
  loading?: boolean
  total: number
}

const SourcesTable: React.FC<SourcesTableProps> = ({
  sources,
  workspaceId,
  loading,
  total,
}) => {
  const { routePrefix } = useWorkspace()
  const navigate = useNavigate()

  return (
    <Table sx={{ mb: -1 }}>
      <TableHead>
        <TableRow>
          <TableCell>Name</TableCell>
          <TableCell sx={{ width: 0, textAlign: "right" }}>Nodes</TableCell>
          <TableCell sx={{ width: 0, textAlign: "right" }}>Edges</TableCell>
          <TableCell />
          <TableCell>Connections</TableCell>
          <TableCell sx={{ width: 0 }} />
        </TableRow>
      </TableHead>
      <TableBody>
        {sources.map(source => (
          <TableRow
            key={source.id}
            hover
            sx={{ cursor: "pointer" }}
            onClick={() => navigate(source.id)}
          >
            <TableCell>{source.name}</TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              {source.nodes.meta.total}
            </TableCell>
            <TableCell sx={{ textAlign: "right" }}>
              {source.edges.meta.total}
            </TableCell>
            <TableCell />
            <TableCell sx={{ p: 1 }} stopPropagation>
              {source.connections.data.map(connection => (
                <Card
                  key={connection.id}
                  sx={{
                    boxShadow: "0px 8px 20px rgba(0, 0, 0, 0.06)",
                    borderWidth: 1,
                    borderStyle: "solid",
                    borderRadius: "12px",
                    borderColor: "rgba(0, 0, 0, 0.08)",
                  }}
                >
                  <CardActionArea
                    component={Link}
                    to={`${routePrefix}/connections/${connection.id}`}
                    sx={{ display: "flex", alignItems: "center", pr: 1 }}
                  >
                    <ConnectorIcon connector={connection.connector} noBorder />
                    <Typography variant="body2" sx={{ ml: 1, flexGrow: 1 }}>
                      {connection.name}
                    </Typography>
                    {connection.last_run && (
                      <RunStatus
                        run={connection.last_run}
                        size="small"
                        link
                        sx={{ cursor: "pointer" }}
                      />
                    )}
                  </CardActionArea>
                </Card>
              ))}
            </TableCell>
            <TableCell sx={{ py: 0, px: 1 }} stopPropagation>
              <SourcesMenu source={source} workspaceId={workspaceId} />
            </TableCell>
          </TableRow>
        ))}
        {!loading && sources.length === 0 && (
          <TableRow>
            <TableCell colSpan={99} sx={{ textAlign: "center", py: 10 }}>
              <Typography>No sources found</Typography>
            </TableCell>
          </TableRow>
        )}
        {loading && (
          <TableRow>
            <TableCell colSpan={99}>
              <Loading />
            </TableCell>
          </TableRow>
        )}
      </TableBody>
      <TableFooter>
        <TablePagination
          count={total}
          rowsPerPage={1000}
          page={0}
          type="sources"
        />
      </TableFooter>
    </Table>
  )
}

export default SourcesTable
