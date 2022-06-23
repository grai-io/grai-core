// src/@chakra-ui/gatsby-plugin/theme.js
// gatsby shadow
import { extendTheme, theme as base } from "@chakra-ui/react"
import { createBreakpoints } from "@chakra-ui/theme-tools"

const breakpoints = createBreakpoints({
  sm: "428px",
  md: "768px",
  lg: "960px",
  xl: "1200px",
  "2xl": "1440",
  "3xl": "1600",
  "4xl": "1920",
})

const theme = {
  colors: {
    polo: "#BFD2EB",
    pololight: "#E5ECF4",
    mango: "#FFB567",
    mangolight: "#F9DEC3",
    kobi: "#F1D7E0",
    kobilight: "#FEF2F6",
    bastille: "#351D36",
    soapstone: "#FFFFFF"
  },
  fonts: {
    heading: `Cabinet Grotesk, ${base.fonts?.heading}`,
    body: "Satoshi"
  },
  fontSizes:{
    sm: "0.875rem",
    md: "1rem",
    lg: "1.125rem",
    xl: "1.25rem",
    "2xl": "1.5rem",
    "3xl": "1.875rem",
    "4xl": "2.25rem",
  },
  initialColorMode: "light",
  useSystemColorMode: false,
  breakpoints,
}

export default extendTheme(theme)
