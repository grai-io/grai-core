import React from "react"
import { Box, Card } from "@mui/material"

interface Connector {
  name: string
  icon: string | null
}

interface Connection {
  connector: Connector
}

interface Report {
  id: string
  connection: Connection
}

type ReportCardProps = {
  report: Report
}

const ReportCard: React.FC<ReportCardProps> = ({ report }) => {
  return (
    <Card sx={{ height: "120px", p: "24px", display: "flex" }}>
      <Box sx={{ borderRadius: "50%", backgroundColor: "#F8F8F8" }}>
        {report.connection.connector.icon && (
          <img
            src={report.connection.connector.icon}
            alt={report.connection.connector.name}
            width={64}
            height={64}
          />
        )}
      </Box>
      {report.id}
    </Card>
  )
}

export default ReportCard
