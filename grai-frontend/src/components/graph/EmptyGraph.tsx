import React from "react"
import { Box, Typography, Button } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

const EmptyGraph: React.FC = () => {
  const { routePrefix } = useWorkspace()

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100%",
        flexDirection: "column",
      }}
    >
      <Typography sx={{ pb: 3 }}>Your graph is empty!</Typography>
      <Typography>
        To get started{" "}
        <Button
          component={Link}
          to={`${routePrefix}/connections/create`}
          variant="outlined"
          sx={{ ml: 1 }}
        >
          Add Connection
        </Button>
      </Typography>
    </Box>
  )
}

export default EmptyGraph
