import { createTheme } from "@mui/material/styles"

// declare module '@material-ui/core/styles/createPalette' {
//   interface Palette {
//       pgrey: Palette['primary']
//   }
//   interface PaletteOptions {
//       pgrey: PaletteOptions['primary']
//   }
// }

const theme = createTheme({
  typography: {
    fontFamily: `"Sora", "Satoshi", "Roboto", "Helvetica", "Arial", sans-serif`,
  },
  palette: {
    primary: {
      main: "#351D36",
      contrastText: "white",
    },
    secondary: {
      main: "#FFB567",
    },
    // pgrey: {
    //     main: '#aaabb8',
    // },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "inherit",
        },
        containedPrimary: {
          "&:hover": {
            backgroundColor: "#1AC9FF",
          },
        },
      },
    },
    MuiTab: {
      styleOverrides: {
        root: {
          textTransform: "inherit",
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          "& th": {
            fontWeight: 700,
          },
        },
      },
    },
  },
})

export default theme
