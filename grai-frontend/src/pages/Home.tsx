import { Search } from "@mui/icons-material"
import {
  Box,
  Container,
  InputAdornment,
  TextField,
  Typography,
} from "@mui/material"
import React from "react"
import HomeCards from "components/home/HomeCards"
import AppTopBar from "components/layout/AppTopBar"

const Home: React.FC = () => (
  <>
    <AppTopBar />
    <Container maxWidth="lg" sx={{ textAlign: "center" }}>
      <Box sx={{ mt: 15 }}>
        <img src="/logo512.png" width="75px" height="75px" alt="logo" />
      </Box>

      <Typography variant="h4" sx={{ mt: 2, mb: 15 }}>
        Welcome to Grai
      </Typography>
      <TextField
        placeholder="Search data assets"
        sx={{ width: 750, mb: 15 }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Search />
            </InputAdornment>
          ),
        }}
      />
      <HomeCards />
    </Container>
  </>
)

export default Home
