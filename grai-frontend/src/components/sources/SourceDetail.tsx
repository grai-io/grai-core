import React from "react"
import { Add } from "@mui/icons-material"
import { Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import SourceConnectionsTable, { Connection } from "./SourceConnectionsTable"
import UpdateSource, { Source as UpdateSourceType } from "./UpdateSource"

interface Source extends UpdateSourceType {
  connections: {
    data: Connection[]
  }
}

type SourceDetailProps = {
  source: Source
  workspaceId: string
}

const SourceDetail: React.FC<SourceDetailProps> = ({ source, workspaceId }) => {
  const { routePrefix } = useWorkspace()

  const connections = source.connections.data

  return (
    <>
      <PageContent>
        <UpdateSource source={source} />
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
        <SourceConnectionsTable
          connections={connections}
          workspaceId={workspaceId}
        />
      </PageContent>
    </>
  )
}

export default SourceDetail
