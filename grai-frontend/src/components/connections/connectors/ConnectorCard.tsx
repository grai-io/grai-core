import React, { ReactNode } from "react"
import {
  Box,
  Card,
  CardActionArea,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
} from "@mui/material"
import { useNavigate } from "react-router-dom"
import useWorkspace from "helpers/useWorkspace"
import ConnectorIcon from "./ConnectorIcon"

export interface Connector {
  id: string
  name: string
  icon: string | null | ReactNode
  status?: string
  metadata: any
  to?: string
}

type ConnectorCardProps = {
  connector: Connector
}

const ConnectorCard: React.FC<ConnectorCardProps> = ({ connector }) => {
  const navigate = useNavigate()
  const { routePrefix } = useWorkspace()

  const comingSoon = connector.status === "coming_soon"

  return (
    <Box>
      <Card
        variant="outlined"
        sx={{
          borderRadius: "20px",
          border: comingSoon ? "1px solid rgba(0, 0, 0, 0.08)" : undefined,
          height: "88px",
        }}
      >
        <CardActionArea
          onClick={() =>
            navigate(
              connector.to ??
                `${routePrefix}/connections/create?connectorId=${connector.id}`,
            )
          }
          sx={{ height: "100%" }}
        >
          <List>
            <ListItem sx={{ pl: "20px" }}>
              <ListItemIcon sx={{ minWidth: 48 }}>
                {connector.icon && <ConnectorIcon connector={connector} />}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Typography
                    variant="body1"
                    sx={{
                      fontWeight: 500,
                      color: comingSoon ? "#AFAFAF" : undefined,
                    }}
                  >
                    {connector.name}
                  </Typography>
                }
              />
            </ListItem>
          </List>
        </CardActionArea>
      </Card>
      {connector.status &&
        ["coming_soon", "alpha"].includes(connector.status) && (
          <Box
            sx={{
              position: "relative",
              top: -105,
              right: comingSoon ? -220 : -275,
              width: "fit-content",
              textAlign: "center",
              px: "12px",
              py: "6px",
              borderRadius: "100px",
              background: "#f4edff",
            }}
          >
            <Typography
              variant="body2"
              sx={{
                textTransform: "capitalize",
              }}
            >
              {connector.status?.replace("_", " ")}
            </Typography>
          </Box>
        )}
    </Box>
  )
}

export default ConnectorCard
