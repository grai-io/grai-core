import { Typography } from "@mui/material"
import React, { useEffect, useState } from "react"
import AppTopBar from "../../components/layout/AppTopBar"
import NodesTable from "../../components/nodes/NodesTable"
import useAxios from "../../utils/useAxios"

export interface Node {
  id: string
  namespace: string
  name: string
  display_name: string
  data_source: string
  is_active: boolean
  metadata: any
}

const Nodes: React.FC = () => {
  const [res, setRes] = useState<Node[] | null>()
  const [error, setError] = useState<string>()
  const api = useAxios()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/lineage/nodes")
        setRes(response.data)
      } catch {
        setError("Something went wrong")
      }
    }
    fetchData()
  }, [])

  return (
    <>
      <AppTopBar />
      <Typography variant="h4" sx={{ textAlign: "center", m: 3 }}>
        Nodes
      </Typography>
      <NodesTable nodes={res ?? null} />
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Nodes
