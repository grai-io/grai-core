import React from "react"
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  Divider,
} from "@mui/material"
import { Link } from "react-router-dom"

type HomeCardProps = {
  title: string
  description: string
  button: string
  to: string
}

const HomeCard: React.FC<HomeCardProps> = ({
  title,
  description,
  button,
  to,
}) => (
  <Card
    variant="outlined"
    sx={{
      borderRadius: 0,
      display: "flex",
      flexDirection: "column",
      height: "100%",
    }}
  >
    <CardContent sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h5" sx={{ mb: 3, fontWeight: "bold" }}>
        {title}
      </Typography>
      <Typography variant="body1">{description}</Typography>
    </CardContent>
    <Divider sx={{ mx: 2 }} />
    <Box sx={{ textAlign: "center", py: 3 }}>
      <Button variant="contained" color="secondary" component={Link} to={to}>
        {button}
      </Button>
    </Box>
  </Card>
)

export default HomeCard
