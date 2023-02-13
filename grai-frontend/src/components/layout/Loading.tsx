import React from "react"
import { Box, CircularProgress, Typography } from "@mui/material"

type LoadingProps = {
  message?: string
}

const Loading: React.FC<LoadingProps> = ({ message }) => (
  <Box
    sx={{
      position: "absolute",
      top: "50%",
      left: "50%",
      transform: "translate(-50%, -50%)",
      textAlign: "center",
    }}
  >
    <CircularProgress />
    {message && (
      <Typography variant="body1" sx={{ mt: 3 }}>
        {message}
      </Typography>
    )}
  </Box>
)

export default Loading
