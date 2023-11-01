import React from "react"
import { Typography, Box } from "@mui/material"

type WizardSubtitleProps = {
  title?: string | null
  subTitle?: string | null
}

const WizardSubtitle: React.FC<WizardSubtitleProps> = ({ title, subTitle }) => (
  <Box>
    <Typography
      variant="h6"
      sx={{
        color: "#1F2A37",
        fontSize: 22,
        fontWeight: 800,
        lineHeight: "150%",
        letterSpacing: "0.22px",
        mb: "14px",
      }}
    >
      {title}
    </Typography>
    <Typography>{subTitle}</Typography>
  </Box>
)

export default WizardSubtitle
