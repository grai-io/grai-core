import React from "react"
import { Box, Button, Typography } from "@mui/material"
import QRCode from "react-qr-code"

type CodeProps = {
  config_url: string
  onNext: () => void
}

const Code: React.FC<CodeProps> = ({ config_url, onNext }) => (
  <Box sx={{ textAlign: "center", mb: 5 }}>
    <Typography sx={{ pt: 2 }}>
      Scan the qr code with an authenticator app
    </Typography>

    <Box sx={{ px: 10, py: 7 }}>
      <QRCode value={config_url} />
    </Box>
    <Button onClick={onNext} variant="contained" size="large">
      Next
    </Button>
  </Box>
)

export default Code
