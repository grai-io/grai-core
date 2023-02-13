import { Stack, Box, Button, Typography } from "@mui/material"
import NodeDetailRow from "components/layout/NodeDetailRow"
import useWorkspace from "helpers/useWorkspace"
import React from "react"
import { Link } from "react-router-dom"

interface Dependency {
  id: string
  display_name: string
}

type TableDependenciesProps = {
  label: string
  dependencies: Dependency[]
}

const TableDependencies: React.FC<TableDependenciesProps> = ({
  label,
  dependencies,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <NodeDetailRow label={label}>
      {dependencies.length > 0 ? (
        <Stack>
          {dependencies.map(table => (
            <Box key={table.id}>
              <Button component={Link} to={`${routePrefix}/tables/${table.id}`}>
                {table.display_name}
              </Button>
            </Box>
          ))}
        </Stack>
      ) : (
        <Typography variant="body2">None</Typography>
      )}
    </NodeDetailRow>
  )
}

export default TableDependencies
