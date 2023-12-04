import React from "react"
import { Box } from "@mui/material"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import ConnectionToolbar from "./ConnectionToolbar"
import ConnectorSelect from "./ConnectorSelect"

const ConnectorSelectTab: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <PageContent noPadding>
      <ConnectionToolbar
        title="Select Integration"
        activeStep={0}
        onBack={`${routePrefix}/sources`}
      />
      <Box sx={{ px: 3 }}>
        <ConnectorSelect />
      </Box>
    </PageContent>
  )
}

export default ConnectorSelectTab
