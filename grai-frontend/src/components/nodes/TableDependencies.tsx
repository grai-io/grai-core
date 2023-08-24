import React from "react"
import { Stack, Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import NodeDetailRow from "components/layout/NodeDetailRow"

interface Dependency {
  id: string
  display_name: string
}

interface Source {
  id: string
  name: string
}

type TableDependenciesProps = {
  label: string
  dependencies: (Dependency | Source)[]
  routePrefix?: string
}

const TableDependencies: React.FC<TableDependenciesProps> = ({
  label,
  dependencies,
  routePrefix,
}) => {
  const { routePrefix: workspaceRoutePrefix } = useWorkspace()

  return (
    <NodeDetailRow label={label}>
      {dependencies.length > 0 ? (
        <Stack>
          {dependencies.map(table => (
            <Box key={table.id}>
              <Button
                component={Link}
                to={`${workspaceRoutePrefix}/${routePrefix ?? "tables"}/${
                  table.id
                }`}
                sx={{ minWidth: 0 }}
              >
                {"display_name" in table ? table.display_name : table.name}
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
