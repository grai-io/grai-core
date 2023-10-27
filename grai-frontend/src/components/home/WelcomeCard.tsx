import React from "react"
import { Search } from "@mui/icons-material"
import {
  Card,
  Box,
  Button,
  Typography,
  TextField,
  InputAdornment,
} from "@mui/material"
import { Link } from "react-router-dom"
import { GraiLogo, PersonAdd } from "components/icons"

type WelcomeCardProps = {
  search: boolean
  setSearch: (search: boolean) => void
}

const WelcomeCard: React.FC<WelcomeCardProps> = ({ search, setSearch }) => (
  <Card
    elevation={0}
    sx={{
      borderRadius: "20px",
      borderColor: "#8338EC",
      borderWidth: "3px",
      borderStyle: "solid",
      padding: "16px",
      height: "470px",
      mb: "24px",
      position: "relative",
    }}
  >
    <Box
      sx={{
        backgroundColor: "#8338EC20",
        width: 569,
        height: 444,
        position: "absolute",
        top: 252,
        left: -200,
        borderRadius: "50%",
        filter: "blur(200px)",
      }}
    />
    <Box
      sx={{
        backgroundColor: "#3A86FF20",
        width: 569,
        height: 444,
        position: "absolute",
        top: -300,
        right: -300,
        borderRadius: "50%",
        filter: "blur(200px)",
        overflow: "hidden",
      }}
    />
    <Box sx={{ display: "flex" }}>
      <Box sx={{ flexGrow: 1 }} />
      <Button
        component={Link}
        to="settings/memberships"
        variant="outlined"
        startIcon={<PersonAdd />}
        sx={{
          color: "#8338EC",
          fontSize: "16px",
          fontWeight: 600,
          borderColor: "#8338EC24",
          borderRadius: "8px",
          py: 1,
          px: 3,
          boxShadow: "0 4px 6px #8338EC10",
          backgroundColor: "white",
        }}
      >
        Invite User
      </Button>
    </Box>
    <Box sx={{ textAlign: "center" }}>
      <Box>
        <GraiLogo />
      </Box>
      <Typography
        variant="h4"
        sx={{
          color: "#1F2A37",
          fontSize: 36,
          fontWeight: 800,
          mt: "20px",
        }}
      >
        Welcome to Grai
      </Typography>

      {/* <TextField
        placeholder="Search data assets"
        onMouseDown={() => setSearch(true)}
        disabled
        sx={{
          width: 620,
          mb: 15,
          mt: "100px",
          input: {
            "&::placeholder": {
              opacity: 1,
            },
          },
        }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <Search />
            </InputAdornment>
          ),
        }}
      /> */}
    </Box>
  </Card>
)

export default WelcomeCard
