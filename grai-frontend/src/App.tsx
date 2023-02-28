import React from "react"
import { Close } from "@mui/icons-material"
import { CssBaseline, IconButton, ThemeProvider } from "@mui/material"
import { SnackbarKey, SnackbarProvider } from "notistack"
import { BrowserRouter } from "react-router-dom"
import PosthogProvider from "components/PosthogProvider"
import BackendProvider from "./providers/BackendProvider"
import Routes from "./Routes"
import theme from "./theme"
import "posthog"

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
              <PosthogProvider />
              <Routes />
            </BrowserRouter>
          </SnackbarProvider>
        </BackendProvider>
      </ThemeProvider>
    </div>
  )
}

export default App
