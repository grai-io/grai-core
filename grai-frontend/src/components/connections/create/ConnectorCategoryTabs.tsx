import React from "react"
import { Tab, Tabs } from "@mui/material"

type ConnectorCategoryTabsProps = {
  categories: string[]
  value: string | null
  onChange: (value: string | null) => void
}

const ConnectorCategoryTabs: React.FC<ConnectorCategoryTabsProps> = ({
  categories,
  value,
  onChange,
}) => {
  return (
    <Tabs value={value} onChange={(_, newValue) => onChange(newValue)}>
      <Tab label="All Integrations" value={null} />
      {categories.map(category => (
        <Tab
          label={category}
          value={category}
          key={category}
          sx={{ textTransform: "capitalize" }}
        />
      ))}
    </Tabs>
  )
}

export default ConnectorCategoryTabs
