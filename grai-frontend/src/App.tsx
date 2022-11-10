import { CssBaseline, ThemeProvider } from "@mui/material"
import React from "react"
import "./App.css"
import Routes from "./Routes"
import theme from "./theme"

const App = () => {
  return (
    <div className="App">
      <CssBaseline />
      <ThemeProvider theme={theme}>
        <Routes />
      </ThemeProvider>
    </div>
  )
}

export default App
