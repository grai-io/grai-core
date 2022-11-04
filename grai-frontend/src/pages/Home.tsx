import { Box, Typography } from "@mui/material"
import React, { useEffect, useState } from "react"
import useAxios from "../utils/useAxios"
import { Edge } from "./edges/Edges"
import { Node } from "./nodes/Nodes"
import Graph from "../components/home/Graph"
import AppTopBar from "../components/layout/AppTopBar"

const Home: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>()
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

  return (
    <>
      <AppTopBar />
      {nodes && edges && (
        <Box sx={{ height: "calc(100vh - 68px)", width: "100%" }}>
          <Graph nodes={nodes} edges={edges} />
        </Box>
      )}
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Home
