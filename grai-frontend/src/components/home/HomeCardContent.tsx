import React, { ReactNode } from "react"
import { KeyboardArrowRight } from "@mui/icons-material"
import { CardContent, Box, alpha, Typography } from "@mui/material"

export type HomeCardContentProps = {
  count?: number
  icon?: ReactNode
  color: string
  text: string
  to?: string
}

const HomeCardContent: React.FC<HomeCardContentProps> = ({
  count,
  icon,
  color,
  text,
  to,
}) => (
  <CardContent sx={{ p: 3, display: "flex", alignItems: "center" }}>
    <Box
      sx={{
        color,
        backgroundColor: alpha(color, 0.12),
        width: "72px",
        height: "72px",
        borderRadius: "50%",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        mr: 3,
      }}
    >
      {count && (
        <Typography sx={{ fontSize: 38, fontWeight: "bold" }}>
          {count}
        </Typography>
      )}
      {icon}
    </Box>
    <Typography
      variant="h5"
      sx={{
        fontSize: 14,
        fontWeight: to ? "bold" : 500,
        color: to ? color : "#818792",
        flexGrow: 1,
      }}
    >
      {text}
    </Typography>
    {to && <KeyboardArrowRight sx={{ color }} />}
  </CardContent>
)

export default HomeCardContent
