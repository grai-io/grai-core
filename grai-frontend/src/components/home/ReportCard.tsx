import React from "react"
import { Box, Card, CardActionArea, Typography } from "@mui/material"
import { Link } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"

interface Connector {
  name: string
  icon: string | null
}

interface Connection {
  name: string
  connector: Connector
  temp: boolean
}

interface Report {
  id: string
  connection: Connection
}

type ReportCardProps = {
  report: Report
}

const ReportCard: React.FC<ReportCardProps> = ({ report }) => {
  const { routePrefix } = useWorkspace()

  return (
    <Card
      sx={{
        borderRadius: "20px",
        borderStyle: "solid",
        borderWidth: 1,
        borderColor: "#00000008",
        boxShadow: "0 4px 16px 0 rgba(0, 0, 0, 0.10)",
      }}
      elevation={0}
    >
      <CardActionArea
        component={Link}
        to={`${routePrefix}/reports/${report.id}`}
      >
        <Box sx={{ p: "24px", display: "flex" }}>
          <Box
            sx={{
              borderRadius: "50%",
              backgroundColor: "#F8F8F8",
              width: "64px",
              height: "64px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            {report.connection.connector.icon && (
              <img
                src={report.connection.connector.icon}
                alt={report.connection.connector.name}
                width={36}
                height={36}
              />
            )}
          </Box>
          <Box sx={{ ml: "16px" }}>
            <Typography sx={{ fontWeight: "bold", fontSize: "16px", pt: 1 }}>
              {report.connection.temp
                ? report.connection.connector.name
                : report.connection.name}
            </Typography>
            <Typography sx={{ pt: 0.5 }}>grai-io/grai-core</Typography>
          </Box>
        </Box>
      </CardActionArea>
    </Card>
  )
}

export default ReportCard
