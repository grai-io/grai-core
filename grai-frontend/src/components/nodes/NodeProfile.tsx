import {
  Card,
  Grid,
  Typography,
  Table,
  TableBody,
  Stack,
  Button,
  Box,
} from "@mui/material"
import React from "react"
import NodeColumns from "./NodeColumns"
import NodeDetail from "./NodeDetail"
import { Edge, Node as NodeType, nodeToTable } from "helpers/graph"
import NodeDetailRow from "./NodeDetailRow"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

export interface Node extends NodeType {
  id: string
  name: string
  display_name: string
}

type NodeProfileProps = {
  node: Node
  nodes: NodeType[]
  edges: Edge[]
}

const NodeProfile: React.FC<NodeProfileProps> = ({ node, nodes, edges }) => {
  const { routePrefix } = useWorkspace()

  const table = nodeToTable<NodeType>(node, nodes, edges)

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
                  {table.destinationTables.length > 0 ? (
                    <Stack>
                      {table.destinationTables?.map(table => (
                        <Box key={table.id}>
                          <Button
                            component={Link}
                            to={`${routePrefix}/nodes/${table.id}`}
                          >
                            {table.display_name}
                          </Button>
                        </Box>
                      ))}
                    </Stack>
                  ) : (
                    <Typography variant="body2">None</Typography>
                  )}
                </NodeDetailRow>
                <NodeDetailRow label="Downstream dependencies">
                  {table.sourceTables.length > 0 ? (
                    <Stack>
                      {table.sourceTables.map(table => (
                        <Box key={table.id}>
                          <Button
                            component={Link}
                            to={`${routePrefix}/nodes/${table.id}`}
                          >
                            {table.display_name}
                          </Button>
                        </Box>
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
      <NodeColumns columns={table.columns} />
    </>
  )
}

export default NodeProfile
