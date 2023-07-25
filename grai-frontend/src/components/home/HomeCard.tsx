import React, { ReactNode } from "react"
import { Card, CardActionArea } from "@mui/material"
import { Link } from "react-router-dom"
import HomeCardContent from "./HomeCardContent"

type HomeCardProps = {
  count?: number
  icon?: ReactNode
  color: string
  text: string
  to?: string
}

const HomeCard: React.FC<HomeCardProps> = ({
  count,
  icon,
  color,
  text,
  to,
}) => (
  <Card
    variant="outlined"
    sx={{
      borderRadius: "20px",
      borderWidth: to ? 1 : 0,
      borderColor: "#8338EC24",
      flexDirection: "column",
      height: "100%",
    }}
  >
    {to ? (
      <CardActionArea component={Link} to={to}>
        <HomeCardContent
          count={count}
          icon={icon}
          color={color}
          text={text}
          to={to}
        />
      </CardActionArea>
    ) : (
      <HomeCardContent count={count} icon={icon} color={color} text={text} />
    )}
  </Card>
)

export default HomeCard
