import React from "react"
import { Add, Description } from "@mui/icons-material"
import { Box, Button, Card, Link, Typography } from "@mui/material"
import { Link as RouterLink } from "react-router-dom"

const GettingStarted: React.FC = () => (
  <Card
    elevation={0}
    sx={{
      borderRadius: "20px",
      borderColor: theme => theme.palette.secondary.main,
      borderWidth: "3px",
      borderStyle: "solid",
      padding: "16px",
      my: "24px",
      position: "relative",
      textAlign: "center",
    }}
  >
    <Typography variant="h5" sx={{ my: 5, fontWeight: "bold" }}>
      Getting started with Grai
    </Typography>
    <Box sx={{ my: 5 }}>
      <Button
        variant="outlined"
        sx={{ mr: 2 }}
        component={RouterLink}
        to="connections/create"
        startIcon={<Add />}
      >
        Create first connection
      </Button>
      <Button
        variant="outlined"
        component={Link}
        href="https://docs.grai.io"
        target="_blank"
        startIcon={<Description />}
      >
        Read the docs
      </Button>
    </Box>
  </Card>
)

export default GettingStarted
