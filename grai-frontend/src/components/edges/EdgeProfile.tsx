import React from "react"
import { Box, Button, Card, Grid, Table, TableBody } from "@mui/material"
import { JsonView, defaultStyles } from "react-json-view-lite"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import NodeDetailRow from "components/layout/NodeDetailRow"

interface Node {
  id: string
  name: string
  display_name: string
}

interface Edge {
  id: string
  name: string
  display_name: string
  namespace: string
  is_active: boolean
  metadata: any | null
  source: Node
  destination: Node
}

type EdgeProfileProps = {
  edge: Edge
}

const EdgeProfile: React.FC<EdgeProfileProps> = ({ edge }) => {
  const { routePrefix } = useWorkspace()

  return (
    <Grid container spacing={3}>
      <Grid item md={6}>
        <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
          <Table>
            <TableBody>
              <NodeDetailRow label="Name" value={edge.name} />
              <NodeDetailRow label="Namespace" value={edge.namespace} />
              <NodeDetailRow label="Metadata">
                {edge.metadata && (
                  <JsonView
                    data={edge.metadata}
                    shouldExpandNode={level => level < 1}
                    style={{ ...defaultStyles, container: "" }}
                  />
                )}
              </NodeDetailRow>
            </TableBody>
          </Table>
        </Card>
      </Grid>
      <Grid item md={6}>
        <Card variant="outlined" sx={{ borderRadius: 0, borderBottom: 0 }}>
          <Table>
            <TableBody>
              <NodeDetailRow label="Source">
                <Box>
                  <Button
                    component={Link}
                    to={`${routePrefix}/nodes/${edge.source.id}`}
                  >
                    {edge.source.display_name}
                  </Button>
                </Box>
              </NodeDetailRow>
              <NodeDetailRow label="Destination">
                <Box>
                  <Button
                    component={Link}
                    to={`${routePrefix}/nodes/${edge.destination.id}`}
                  >
                    {edge.destination.display_name}
                  </Button>
                </Box>
              </NodeDetailRow>
            </TableBody>
          </Table>
        </Card>
      </Grid>
    </Grid>
  )
}

export default EdgeProfile
