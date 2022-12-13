import {
  Card,
  Grid,
  Typography,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  Stack,
  Button,
} from "@mui/material"
import React from "react"
import { useNavigate } from "react-router-dom"
import NodeColumns from "./NodeColumns"
import NodeDetail from "./NodeDetail"
import { Node as NodeType } from "../../helpers/graph"
import NodeDetailRow from "./NodeDetailRow"
import { Link } from "react-router-dom"

export interface Node extends NodeType {
  id: string
  name: string
  displayName: string
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
          <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
            <Table>
              <TableBody>
                <NodeDetailRow label="Upstream dependencies">
                  {node.destinationEdges.length > 0 ? (
                    <Stack>
                      {node.destinationEdges?.map(edge => (
                        <Button
                          key={edge.id}
                          component={Link}
                          to={`/nodes/${edge.source.id}`}
                        >
                          {edge.source.displayName}
                        </Button>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2">None</Typography>
                  )}
                </NodeDetailRow>
                <NodeDetailRow label="Downstream dependencies">
                  {outputs.length > 0 ? (
                    <Stack>
                      {outputs.map(edge => (
                        <Button
                          key={edge.id}
                          component={Link}
                          to={`/nodes/${edge.destination.id}`}
                        >
                          {edge.destination.displayName}
                        </Button>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2">None</Typography>
                  )}
                </NodeDetailRow>
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
