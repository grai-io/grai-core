import {
  Card,
  CardContent,
  CircularProgress,
  Container,
  Grid,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material"
import React, { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import AppTopBar from "../../components/layout/AppTopBar"
import useAxios from "../../utils/useAxios"
import { Edge } from "../edges/Edges"
import { Node as NodeType } from "./Nodes"

const Node: React.FC = () => {
  const [nodes, setNodes] = useState<NodeType[]>()
  const [edges, setEdges] = useState<Edge[]>()
  const [error, setError] = useState<string>()
  const api = useAxios()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const responseNodes = await api.get("/lineage/nodes")
        setNodes(responseNodes.data)

        const responseEdges = await api.get("/lineage/edges")
        setEdges(responseEdges.data)
      } catch {
        setError("Something went wrong")
      }
    }
    fetchData()
  }, [])

  const params = useParams()
  const navigate = useNavigate()

  const node = nodes?.find(n => n.id === params.nodeId)

  if (!node)
    return (
      <>
        <CircularProgress />
      </>
    )

  const fetchNode = (id: string) => nodes?.find(n => n.id === id)

  const inputEdges = edges
    ?.filter(e => e.destination === node.id)
    .map(e => ({
      ...e,
      node: fetchNode(e.source),
    }))
  const outputEdges = edges
    ?.filter(e => e.source === node.id)
    .map(e => ({
      ...e,
      node: fetchNode(e.destination),
    }))

  return (
    <>
      <AppTopBar />
      {nodes && edges ? (
        <Container maxWidth="md" sx={{ my: 5 }}>
          <Typography variant="h5" sx={{ my: 5, textAlign: "center" }}>
            Node {node?.display_name ?? node?.id}
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
                        {typeof value === "string"
                          ? value
                          : value
                          ? "yes"
                          : "no"}
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
                {inputEdges?.map(edge => (
                  <TableRow
                    key={edge.id}
                    onClick={() => navigate(`/nodes/${edge.node?.id}`)}
                    hover
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <TableCell>{edge.source}</TableCell>
                    <TableCell>{edge.node?.display_name}</TableCell>
                    <TableCell>{edge.node?.metadata.node_type}</TableCell>
                  </TableRow>
                ))}
                {inputEdges?.length === 0 && (
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
                {outputEdges?.map(edge => (
                  <TableRow
                    key={edge.id}
                    onClick={() => navigate(`/nodes/${edge.node?.id}`)}
                    hover
                    sx={{
                      cursor: "pointer",
                    }}
                  >
                    <TableCell>{edge.source}</TableCell>
                    <TableCell>{edge.node?.display_name}</TableCell>
                    <TableCell>{edge.node?.metadata.node_type}</TableCell>
                  </TableRow>
                ))}
                {outputEdges?.length === 0 && (
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
      ) : (
        <CircularProgress />
      )}

      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Node
