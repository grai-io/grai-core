import React, { ReactNode } from "react"
import { Box, Typography } from "@mui/material"

type HelpItemProps = {
  title: string
  icon?: ReactNode
  color?: string
  children?: ReactNode
}

const HelpItem: React.FC<HelpItemProps> = ({
  title,
  icon,
  color,
  children,
}) => (
  <Box sx={{ mb: 5 }}>
    <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
      {icon && (
        <Box
          sx={{
            backgroundColor: color,
            width: "44px",
            height: "44px",
            borderRadius: "44px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            mr: "12px",
          }}
        >
          {icon}
        </Box>
      )}
      <Typography sx={{ color: "#1F2A37", fontWeight: 700 }}>
        {title}
      </Typography>
    </Box>
    <Typography
      variant="body2"
      sx={{ mt: "26px", color: "#999", fontWeight: 700 }}
    >
      {children}
    </Typography>
  </Box>
)

export default HelpItem
