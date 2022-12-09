import React from "react"
import { CssBaseline, ThemeProvider } from "@mui/material"
import Routes from "./Routes"
import theme from "./theme"
import { AuthProvider } from "./components/auth/AuthContext"
import { BrowserRouter } from "react-router-dom"
import BackendProvider from "./providers/BackendProvider"

const App = () => (
  <div>
    <CssBaseline />
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <BackendProvider>
          <BrowserRouter>
            <Routes />
          </BrowserRouter>
        </BackendProvider>
      </AuthProvider>
    </ThemeProvider>
  </div>
)

export default App
