import React from "react"
import { Grid } from "@mui/material"
import { Connections2 } from "components/icons"
import HomeCard from "./HomeCard"

const HomeCards: React.FC = () => (
  <Grid container spacing={3}>
    <Grid item md={3}>
      <HomeCard count={1} text="Currently failing tests" color="#F05252" />
    </Grid>
    <Grid item md={3}>
      <HomeCard count={2} text="Currently failing pipelines" color="#F05252" />
    </Grid>
    <Grid item md={3}>
      <HomeCard count={32} text="Passing tests" color="#31C48D" />
    </Grid>
    <Grid item md={3}>
      <HomeCard
        text="Add Connection"
        color="#8338EC"
        icon={<Connections2 />}
        to="connections/create"
      />
    </Grid>
  </Grid>
)

export default HomeCards
