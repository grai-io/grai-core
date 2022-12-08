import React from "react"
import { gql, useQuery } from "@apollo/client"
import {
  Card,
  CardContent,
  Container,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import { useNavigate, useParams } from "react-router-dom"
import AppTopBar from "../../components/layout/AppTopBar"
import Loading from "../../components/layout/Loading"
import NotFound from "../NotFound"

const GET_NODE = gql`
  query GetNode($nodeId: ID!) {
    node(pk: $nodeId) {
      id
      namespace
      name
      displayName
      isActive
      dataSource
      sourceEdge {
        id
        isActive
        dataSource
        source {
          id
          name
          displayName
          metadata
        }
        metadata
      }
      destinationEdge {
        id
        isActive
        dataSource
        destination {
          id
          name
          displayName
          metadata
        }
        metadata
      }
      metadata
    }
  }
`

const Node: React.FC = () => {
  const params = useParams()
  const navigate = useNavigate()

  const { loading, error, data } = useQuery(GET_NODE, {
    variables: {
      nodeId: params.nodeId,
    },
  })

  if (error) return <p>Error : {error.message}</p>
  if (loading) return <Loading />

  const node = data.node

  if (!node) return <NotFound />

  return (
    <>
      <AppTopBar />

      <Container maxWidth="md" sx={{ my: 5 }}>
        <Typography variant="h5" sx={{ my: 5, textAlign: "center" }}>
          Node {node?.displayName ?? node?.id}
        </Typography>
        <Card variant="outlined" sx={{ my: 5 }}>
          <CardContent>
            <Grid container spacing={1}>
              <Grid item md={2}>
                <Typography variant="caption">name</Typography>
              </Grid>
              <Grid item md={4}>
                <Typography variant="body2">{node.name}</Typography>
              </Grid>
              <Grid item md={2}>
                <Typography variant="caption">id</Typography>
              </Grid>
              <Grid item md={4}>
                <Typography variant="body2">{node.id}</Typography>
              </Grid>
              {Object.entries(node.metadata).map(([key, value]) => (
                <React.Fragment key={key}>
                  <Grid item md={2}>
                    <Typography variant="caption">{key}</Typography>
                  </Grid>
                  <Grid item md={4}>
                    <Typography variant="body2">
                      {typeof value === "string" ? value : value ? "yes" : "no"}
                    </Typography>
                  </Grid>
                </React.Fragment>
              ))}
            </Grid>
          </CardContent>
        </Card>
        <Typography variant="h6" sx={{ m: 1 }}>
          Inputs
        </Typography>
        <Card variant="outlined">
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>id</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {node.sourceEdge?.map((edge: any) => (
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
              {node.sourceEdge?.length === 0 && (
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
        <Card variant="outlined">
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>id</TableCell>
                <TableCell>Name</TableCell>
                <TableCell>Type</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {node.destinationEdge?.map((edge: any) => (
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
                  <TableCell>{edge.destination?.metadata.node_type}</TableCell>
                </TableRow>
              ))}
              {node.destinationEdge?.length === 0 && (
                <TableRow>
                  <TableCell colSpan={3} sx={{ textAlign: "center" }}>
                    No Outputs
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </Card>
      </Container>
    </>
  )
}

export default Node
