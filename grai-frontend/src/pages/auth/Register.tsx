import React from "react"
import { Box, Container, Grid } from "@mui/material"
import { Helmet } from "react-helmet-async"
import LoginLink from "components/auth/register/LoginLink"
import RegisterCard from "components/auth/register/RegisterCard"
import ValueProp from "components/auth/register/ValueProp"
import GraiLogo from "components/icons/GraiLogo"

const Register: React.FC = () => (
  <>
    <Helmet>
      <title>Grai Cloud Register</title>
      <meta
        name="description"
        content="Register for Grai Cloud. The easiest way to get started with data lineage. Create a free account today."
      />
    </Helmet>
    <Box
      sx={{
        width: "100%",
        height: "100vh",
        overflowX: "hidden",
        position: "relative",
      }}
    >
      <Container sx={{ pt: { xs: 3, md: 10 } }} maxWidth="lg">
        <Box sx={{ mb: 3, ml: -1 }}>
          <GraiLogo />
        </Box>
        <Grid container spacing={16}>
          <Grid item xs={0} md={6} display={{ xs: "none", md: "block" }}>
            <ValueProp />
          </Grid>
          <Grid item xs={12} md={6}>
            <RegisterCard />
            <LoginLink />
          </Grid>
        </Grid>
      </Container>
      <Box
        sx={{
          backgroundColor: "#8338EC20",
          width: 810,
          height: 568,
          position: "absolute",
          top: 490,
          left: -318,
          borderRadius: "50%",
          filter: "blur(200px)",
          zIndex: -1,
        }}
      />
      <Box
        sx={{
          backgroundColor: "#3A86FF20",
          width: 800,
          height: 624,
          position: "absolute",
          top: 557,
          right: -300,
          borderRadius: "50%",
          filter: "blur(200px)",
          overflow: "hidden",
          zIndex: -1,
        }}
      />
    </Box>
  </>
)

export default Register
