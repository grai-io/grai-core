import React from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import SourceConfiguration, {
  Source as SourceConfigurationType,
} from "./SourceConfiguration"
import SourceConnectionsTable, {
  Source as SourceConnectionsTableType,
} from "./SourceConnectionsTable"

interface Source extends SourceConfigurationType, SourceConnectionsTableType {}

type SourceDetailProps = {
  source: Source
  workspaceId: string
}

const SourceDetail: React.FC<SourceDetailProps> = ({ source, workspaceId }) => {
  const { routePrefix } = useWorkspace()

  return (
    <>
      <PageContent>
        <SourceConfiguration source={source} />
      </PageContent>
      <PageContent>
        <Box sx={{ display: "flex" }}>
          <Typography sx={{ mb: 2, flexGrow: 1 }}>Connections</Typography>
          <Button
            variant="outlined"
            startIcon={<Add />}
            component={Link}
            to={`${routePrefix}/connections/create?source_id=${source.id}`}
          >
            Add Connection
          </Button>
        </Box>
        <SourceConnectionsTable source={source} workspaceId={workspaceId} />
      </PageContent>
    </>
  )
}

export default SourceDetail
