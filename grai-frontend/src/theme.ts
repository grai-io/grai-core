import { alpha, createTheme } from "@mui/material/styles"

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
    success: {
      main: "#31C48D",
      contrastText: "#1F2A37",
    },
    error: {
      main: "#F05252",
      contrastText: "#1F2A37",
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
    MuiChip: {
      styleOverrides: {
        colorSuccess: theme => ({
          backgroundColor: alpha(theme.theme.palette.success.main, 0.24),
        }),
        colorError: theme => ({
          backgroundColor: alpha(theme.theme.palette.error.main, 0.24),
        }),
      },
    },
  },
})

export default theme
