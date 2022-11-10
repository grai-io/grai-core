import { Typography } from "@mui/material"
import React, { useEffect, useState } from "react"
import EdgesTable from "../../components/edges/EdgesTable"
import AppTopBar from "../../components/layout/AppTopBar"
import useAxios from "../../utils/useAxios"

export interface Edge {
  id: string
  name: string
  namespace: string
  data_source: string
  is_active: boolean
  source: string
  destination: string
  metadata: any
}

const Edges: React.FC = () => {
  const [res, setRes] = useState<Edge[] | null>()
  const [error, setError] = useState<string>()
  const api = useAxios()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/lineage/edges")
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
        Edges
      </Typography>
      <EdgesTable edges={res ?? null} />
      {error && <Typography>{error}</Typography>}
    </>
  )
}

export default Edges
