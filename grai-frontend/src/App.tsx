/* istanbul ignore file */
import React from "react"
import { Close } from "@mui/icons-material"
import { CssBaseline, IconButton, ThemeProvider } from "@mui/material"
import { LocalizationProvider } from "@mui/x-date-pickers"
import { AdapterLuxon } from "@mui/x-date-pickers/AdapterLuxon"
import * as Sentry from "@sentry/react"
import { BrowserTracing } from "@sentry/tracing"
import { ConfirmProvider } from "material-ui-confirm"
import { SnackbarKey, SnackbarProvider } from "notistack"
import {
  BrowserRouter,
  createRoutesFromChildren,
  matchRoutes,
  useLocation,
  useNavigationType,
} from "react-router-dom"
import PosthogProvider from "components/PosthogProvider"
import BackendProvider from "./providers/BackendProvider"
import Routes from "./Routes"
import theme from "./theme"
import "posthog"

const App: React.FC = () => {
  if (process.env.REACT_APP_SENTRY_DSN)
    Sentry.init({
      dsn: process.env.REACT_APP_SENTRY_DSN,
      integrations: [
        new BrowserTracing({
          routingInstrumentation: Sentry.reactRouterV6Instrumentation(
            React.useEffect,
            useLocation,
            useNavigationType,
            createRoutesFromChildren,
            matchRoutes
          ),
        }),
      ],
      tracesSampleRate: 1.0,
    })

  const notistackRef = React.createRef<any>()
  const onClickDismiss = (key: SnackbarKey) => () => {
    notistackRef.current.closeSnackbar(key)
  }

  return (
    <div>
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <LocalizationProvider dateAdapter={AdapterLuxon}>
          <BackendProvider>
            <ConfirmProvider
              defaultOptions={{
                confirmationButtonProps: { autoFocus: true },
              }}
            >
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
            </ConfirmProvider>
          </BackendProvider>
        </LocalizationProvider>
      </ThemeProvider>
    </div>
  )
}

export default App
