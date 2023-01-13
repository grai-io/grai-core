import React from "react"
import { CssBaseline, ThemeProvider } from "@mui/material"
import Routes from "./Routes"
import theme from "./theme"
import { BrowserRouter } from "react-router-dom"
import BackendProvider from "./providers/BackendProvider"

const App = () => (
  <div>
    <CssBaseline />
    <ThemeProvider theme={theme}>
      <BackendProvider>
        <BrowserRouter>
          <Routes />
        </BrowserRouter>
      </BackendProvider>
    </ThemeProvider>
  </div>
)

export default App
