import React from "react"
import { Box, Button, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import PageContent from "components/layout/PageContent"
import ConnectionToolbar from "./ConnectionToolbar"
import { ConnectorType } from "../ConnectionsForm"

type ConnectorComingSoonProps = {
  connector: ConnectorType
}

const ConnectorComingSoon: React.FC<ConnectorComingSoonProps> = ({
  connector,
}) => {
  const { routePrefix } = useWorkspace()

  return (
    <PageContent noPadding>
      <ConnectionToolbar
        title="Setup Connection"
        activeStep={1}
        onBack={`${routePrefix}/connections/create`}
      />
      <Box sx={{ px: 3 }}>
        <Box sx={{ textAlign: "center", pt: 5, pb: 10, borderRadius: "20px" }}>
          <Typography variant="h5">{connector.name} coming soon</Typography>
          <Typography sx={{ mt: 5, lineHeight: "2rem", mb: 10 }}>
            We would love to build this integration for you,
            <br />
            just get in touch on Slack.
          </Typography>
          <Button
            variant="outlined"
            component={Link}
            to={`${routePrefix}/connections/create`}
          >
            Go Back
          </Button>
        </Box>
      </Box>
    </PageContent>
  )
}
export default ConnectorComingSoon
