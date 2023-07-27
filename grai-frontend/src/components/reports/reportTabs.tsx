import { ResultError, Table } from "components/graph/GraphComponent"
import ReportGraph from "./ReportGraph"
import TestResults from "./results/TestResults"
import RunLog, { Run } from "./run/RunLog"

type ReportTabInput = {
  tables: Table[]
  errors: ResultError[] | null
  limitGraph: boolean
  run: Run | null
}

const reportTabs = ({ tables, errors, limitGraph, run }: ReportTabInput) => [
  {
    value: "graph",
    label: "Graph",
    noWrapper: true,
    component: (
      <ReportGraph
        run={run}
        tables={tables}
        errors={errors}
        limitGraph={limitGraph}
      />
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
