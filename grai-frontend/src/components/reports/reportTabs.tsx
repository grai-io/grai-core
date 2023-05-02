import { Box } from "@mui/material"
import { Edge } from "helpers/graph"
import Graph, { Error } from "components/graph/Graph"
import { Table } from "components/graph/MidGraph"
import TestResults from "./results/TestResults"
import RunLog, { Run } from "./run/RunLog"

type ReportTabInput = {
  tables: Table[]
  edges: Edge[]
  errors: Error[] | null
  limitGraph: boolean
  run: Run | null
}

const reportTabs = ({
  tables,
  edges,
  errors,
  limitGraph,
  run,
}: ReportTabInput) => [
  {
    value: "graph",
    label: "Graph",
    noWrapper: true,
    component: (
      <Box
        sx={{
          height: "calc(100vh - 212px)",
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
    component: (
      <TestResults errors={errors?.filter(error => !error.test_pass) ?? null} />
    ),
  },
  {
    value: "all-tests",
    label: "All",
    component: <TestResults errors={errors} />,
  },
  {
    value: "log",
    label: "Log",
    component: run && <RunLog run={run} />,
  },
]

export default reportTabs
