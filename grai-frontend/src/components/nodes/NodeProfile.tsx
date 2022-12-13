import {
  Card,
  Grid,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import NodeColumns from "./NodeColumns"
import NodeDetail from "./NodeDetail"

export interface Node {
  id: string
  name: string
  metadata: any
  destinationEdges: {
    id: string
    source: {
      id: string
      name: string
      displayName: string
      metadata: {
        node_type: string
        table_name: string
      }
    }
  }[]
  sourceEdges: {
    id: string
    destination: {
      id: string
      name: string
      displayName: string
      metadata: {
        node_type: string
        table_name: string
      }
    }
  }[]
}

type NodeProfileProps = {
  node: Node
}

const NodeProfile: React.FC<NodeProfileProps> = ({ node }) => {
  const navigate = useNavigate()

  const outputs = node.sourceEdges?.filter(
    edge =>
      edge.destination.metadata.table_name !== node.metadata.table_name &&
      `public.${edge.destination.metadata.table_name}` !== node.name
  )

  return (
    <>
      <Grid container spacing={3} sx={{ pt: 3 }}>
        <Grid item md={6}>
          <NodeDetail node={node} />
        </Grid>
        <Grid item md={6}>
          <Typography variant="h6" sx={{ m: 1 }}>
            Inputs
          </Typography>
          <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>id</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {node.destinationEdges?.map(edge => (
                  <TableRow
                    key={edge.id}
                    onClick={() => navigate(`/nodes/${edge.source?.id}`)}
                    hover
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <TableCell>
                      {edge.source.displayName ?? edge.source.name}
                    </TableCell>
                    <TableCell>{edge.source?.displayName}</TableCell>
                    <TableCell>{edge.source?.metadata.node_type}</TableCell>
                  </TableRow>
                ))}
                {node.destinationEdges?.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={3} sx={{ textAlign: "center" }}>
                      No Inputs
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Card>
          <Typography variant="h6" sx={{ m: 1, mt: 3 }}>
            Outputs
          </Typography>
          <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>id</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {outputs.map(edge => (
                  <TableRow
                    key={edge.id}
                    onClick={() => navigate(`/nodes/${edge.destination?.id}`)}
                    hover
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <TableCell>
                      {edge.destination.displayName ?? edge.destination.name}
                    </TableCell>
                    <TableCell>{edge.destination?.displayName}</TableCell>
                    <TableCell>
                      {edge.destination?.metadata.node_type}
                    </TableCell>
                  </TableRow>
                ))}
                {outputs.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={3} sx={{ textAlign: "center" }}>
                      No Outputs
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </Card>
        </Grid>
      </Grid>
      <NodeColumns node={node} />
    </>
  )
}

export default NodeProfile
