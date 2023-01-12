import { Box, Typography, Divider } from "@mui/material"
import React from "react"

interface Connector {
  name: string
}

type CreateConnectionHelpProps = {
  connector: Connector | null
}

const CreateConnectionHelp: React.FC<CreateConnectionHelpProps> = ({
  connector,
}) => (
  <Box
    sx={{
      borderLeftWidth: 1,
      borderLeftStyle: "solid",
      borderLeftColor: "divider",
      pl: 3,
    }}
  >
    <Box sx={{ mb: 5 }}>
      <Typography>Read our docs</Typography>
      <Divider sx={{ my: 1 }} />
      <Typography variant="body2">
        Not sure where to start? Check out the docs for {connector?.name} for
        step-by-step instructions.
      </Typography>
    </Box>
    <Box sx={{ mb: 5 }}>
      <Typography>Invite a teammate</Typography>
      <Divider sx={{ my: 1 }} />
      <Typography variant="body2">
        If you're missing credentials or connection info, invite a teammate to
        join you in this Grai workspace.
      </Typography>
    </Box>
    <Box sx={{ mb: 5 }}>
      <Typography>Contact support</Typography>
      <Divider sx={{ my: 1 }} />
      <Typography variant="body2">
        We're here to help! Chat with us if you feel stuck or have any
        questions.
      </Typography>
    </Box>
  </Box>
)

export default CreateConnectionHelp
