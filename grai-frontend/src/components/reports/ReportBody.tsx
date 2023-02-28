import { Box } from "@mui/material"
import Graph, { Error } from "components/graph/Graph"
import Tabs from "components/tabs/Tabs"
import React, { useEffect, useState } from "react"
import TestResults from "./pull_request/TestResults"
import { Table } from "components/graph/MidGraph"
import { Edge } from "helpers/graph"
import { useSearchParams } from "react-router-dom"

type ReportBodyProps = {
  tables: Table[]
  edges: Edge[]
  errors: Error[] | null
}

const ReportBody: React.FC<ReportBodyProps> = ({ tables, edges, errors }) => {
  const [searchParams, setSearchParams] = useSearchParams()
  const [display, setDisplay] = useState(false)

  useEffect(() => {
    setSearchParams({ ...searchParams, limitGraph: "true" })
    setDisplay(true)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  if (!display) return null

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  return (
    <Tabs
      tabs={[
        {
          value: "graph",
          label: "Graph",
          element: (
            <Box
              sx={{
                height: "calc(100vh - 275px)",
                mt: 2,
                width: "100%",
                backgroundColor: theme => theme.palette.grey[100],
              }}
            >
              <Graph
                tables={tables}
                edges={edges}
                errors={errors}
                limitGraph={limitGraph}
              />
            </Box>
          ),
        },
        {
          value: "failed-tests",
          label: "Failed",
          element: <TestResults errors={errors} />,
        },
        {
          value: "all-tests",
          label: "All",
          disabled: true,
        },
      ]}
    />
  )
}

export default ReportBody
