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
import { Helmet, HelmetProvider } from "react-helmet-async"
import {
  BrowserRouter,
  createRoutesFromChildren,
  matchRoutes,
  useLocation,
  useNavigationType,
} from "react-router-dom"
// import { ShepherdTour } from "react-shepherd"
import PosthogProvider from "components/PosthogProvider"
import BackendProvider from "./providers/BackendProvider"
import Routes from "./Routes"
// import steps from "./steps"
import theme from "./theme"
import "posthog"

// const tourOptions = {
//   defaultStepOptions: {
//     cancelIcon: {
//       enabled: true,
//     },
//   },
//   useModalOverlay: true,
// }

const App: React.FC = () => {
  if (process.env.REACT_APP_SENTRY_DSN)
    Sentry.init({
      dsn: process.env.REACT_APP_SENTRY_DSN,
      integrations: [
        new Sentry.Replay(),
        new BrowserTracing({
          routingInstrumentation: Sentry.reactRouterV6Instrumentation(
            React.useEffect,
            useLocation,
            useNavigationType,
            createRoutesFromChildren,
            matchRoutes,
          ),
        }),
      ],
      tracesSampleRate: 1.0,
      replaysSessionSampleRate: 0,
      replaysOnErrorSampleRate: 1.0,
    })

  const notistackRef = React.createRef<any>()
  const onClickDismiss = (key: SnackbarKey) => () => {
    notistackRef.current.closeSnackbar(key)
  }

  return (
    <div>
      <CssBaseline />
      <HelmetProvider>
        <Helmet>
          <title>Grai Cloud</title>
          <meta
            name="description"
            content="The easiest way to get started with data lineage. Create a free account today."
          />
        </Helmet>
        <ThemeProvider theme={theme}>
          <LocalizationProvider dateAdapter={AdapterLuxon}>
            {/* <ShepherdTour steps={steps} tourOptions={tourOptions}> */}
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
            {/* </ShepherdTour> */}
          </LocalizationProvider>
        </ThemeProvider>
      </HelmetProvider>
    </div>
  )
}

export default App
