import React from "react"
import { Grid } from "@mui/material"
import HomeCard from "./HomeCard"

const HomeCards: React.FC = () => (
  <Grid container spacing={3}>
    <Grid item md={4}>
      <HomeCard
        title="Explore data graph"
        description="Discover relevant tables and columns and explore how data flows
            through your pipelines"
        button="Explore graph"
        to="graph"
      />
    </Grid>
    <Grid item md={4}>
      <HomeCard
        title="Add data connections"
        description="Connect your data stores and pipeline tools to collect information
        on your pipelines"
        button="Add connection"
        to="connections/create"
      />
    </Grid>
    <Grid item md={4}>
      <HomeCard
        title="Invite other users"
        description="Invite users to collaborate in Grai"
        button="Invite user"
        to="settings/memberships"
      />
    </Grid>
  </Grid>
)

export default HomeCards
