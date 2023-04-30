import React, { useEffect, useState } from "react"
import { Box } from "@mui/material"
import { useSearchParams } from "react-router-dom"
import { Edge } from "helpers/graph"
import Graph, { Error } from "components/graph/Graph"
import { Table } from "components/graph/MidGraph"
import Tabs from "components/tabs/Tabs"
import ReportResult from "./results/ReportResult"
import TestResults from "./results/TestResults"
import RunLog, { Run } from "./run/RunLog"

type ReportBodyProps = {
  run: Run | null
  tables: Table[]
  edges: Edge[]
  errors: Error[] | null
}

const ReportBody: React.FC<ReportBodyProps> = ({
  run,
  tables,
  edges,
  errors,
}) => {
  const [searchParams, setSearchParams] = useSearchParams()
  const [display, setDisplay] = useState(false)

  useEffect(() => {
    setSearchParams(
      { ...searchParams, limitGraph: "true" },
      {
        replace: true,
      }
    )
    setDisplay(true)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  if (!display) return null

  const limitGraph: boolean =
    searchParams.get("limitGraph")?.toLowerCase() === "true"

  return (
    <>
      <ReportResult errors={errors} />
      <Tabs
        tabs={[
          {
            value: "graph",
            label: "Graph",
            element: (
              <Box
                sx={{
                  height: "calc(100vh - 290px)",
                  mt: 2,
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
            element: (
              <TestResults
                errors={errors?.filter(error => !error.test_pass) ?? null}
              />
            ),
          },
          {
            value: "all-tests",
            label: "All",
            element: <TestResults errors={errors} />,
          },
          {
            value: "log",
            label: "Log",
            element: run && <RunLog run={run} />,
          },
        ]}
      />
    </>
  )
}

export default ReportBody
