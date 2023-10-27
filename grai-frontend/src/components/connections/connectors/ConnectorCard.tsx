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

export interface Connector {
  id: string
  name: string
  icon?: string | null | ReactNode
  status?: string
  metadata: any
  to?: string
}

type ConnectorCardProps = {
  connector: Connector
  onSelect: (connector: Connector) => void
}

const ConnectorCard: React.FC<ConnectorCardProps> = ({
  connector,
  onSelect,
}) => {
  const navigate = useNavigate()

  return (
    <Box>
      <Card variant="outlined">
        <CardActionArea
          onClick={() => {
            if (connector.to) {
              navigate(connector.to)
              return
            }
            onSelect(connector)
          }}
          className="connector-card"
        >
          <List>
            <ListItem>
              <ListItemIcon sx={{ minWidth: 45 }}>
                {connector.icon &&
                  (typeof connector.icon === "string" ? (
                    <img
                      src={connector.icon}
                      alt={`${connector.name} logo`}
                      style={{ height: 28, width: 28 }}
                    />
                  ) : (
                    connector.icon
                  ))}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Typography variant="body2">{connector.name}</Typography>
                }
              />
            </ListItem>
          </List>
        </CardActionArea>
      </Card>
      {connector.status !== "general_release" && (
        <Box
          sx={{
            position: "relative",
            top: -75,
            right: -155,
            width: 130,
            textAlign: "center",
            // height: 100,
            borderWidth: 1,
            borderStyle: "solid",
            borderColor: "divider",
            borderRadius: 1,
            backgroundColor: theme => theme.palette.grey[100],
          }}
        >
          <Typography
            variant="body2"
            sx={{
              m: 0.3,
              color: theme => theme.palette.grey[500],
              textTransform: "uppercase",
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
