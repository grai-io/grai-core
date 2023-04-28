import React from "react"
import { Tab, Tabs } from "@mui/material"

const ConnectionTabs: React.FC = () => (
  <Tabs value="runs" sx={{ mb: "-24px", mt: "24px" }}>
    <Tab value="runs" label="Runs" />
    <Tab value="configuration" label="Configuration" />
    <Tab value="schedule" label="Schedule" />
    <Tab value="activity" label="Activity" disabled />
    <Tab value="alerts" label="Alerts" disabled />
  </Tabs>
)

export default ConnectionTabs
