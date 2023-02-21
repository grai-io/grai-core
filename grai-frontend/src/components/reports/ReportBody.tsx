import { Box } from "@mui/material"
import Graph from "components/graph/Graph"
import Tabs from "components/tabs/Tabs"
import React from "react"
import TestResults from "./pull_request/TestResults"
import { Error } from "components/graph/Graph"
import { Table } from "components/graph/MidGraph"
import { Edge } from "helpers/graph"

type ReportBodyProps = {
  tables: Table[]
  edges: Edge[]
  errors: Error[] | null
}

const ReportBody: React.FC<ReportBodyProps> = ({ tables, edges, errors }) => (
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
            <Graph tables={tables} edges={edges} errors={errors} limitGraph />
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

export default ReportBody
