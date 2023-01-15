import React from "react"
import { CssBaseline, IconButton, ThemeProvider } from "@mui/material"
import Routes from "./Routes"
import theme from "./theme"
import { BrowserRouter } from "react-router-dom"
import BackendProvider from "./providers/BackendProvider"
import { SnackbarKey, SnackbarProvider } from "notistack"
import { Close } from "@mui/icons-material"

const App: React.FC = () => {
  const notistackRef = React.createRef<any>()
  const onClickDismiss = (key: SnackbarKey) => () => {
    notistackRef.current.closeSnackbar(key)
  }

  return (
    <div>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <BackendProvider>
          <SnackbarProvider
            ref={notistackRef}
            maxSnack={3}
            hideIconVariant
            action={key => (
              <IconButton onClick={onClickDismiss(key)}>
                <Close />
              </IconButton>
            )}
          >
            <BrowserRouter>
              <Routes />
            </BrowserRouter>
          </SnackbarProvider>
        </BackendProvider>
      </ThemeProvider>
    </div>
  )
}

export default App
