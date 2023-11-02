import React from "react"
import { Box } from "@mui/material"
import GraphComponent, {
  ResultError,
  Table,
} from "components/graph/GraphComponent"
import { Run } from "./run/RunLog"
import useCombinedFilters from "components/graph/useCombinedFilters"

type ReportGraphProps = {
  tables: Table[]
  errors: ResultError[] | null
  limitGraph: boolean
  run: Run | null
}

const ReportGraph: React.FC<ReportGraphProps> = ({
  tables,
  errors,
  limitGraph,
  run,
}) => {
  const { combinedFilters } = useCombinedFilters(
    `reports-${run?.id}-graph-filters`,
    `reports-${run?.id}-graph-inline-filters`,
  )

  return (
    <Box
      sx={{
        height: "calc(100vh - 212px)",
      }}
    >
      <GraphComponent
        tables={tables}
        errors={errors}
        limitGraph={limitGraph}
        combinedFilters={combinedFilters}
      />
    </Box>
  )
}

export default ReportGraph
