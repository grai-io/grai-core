import React from "react"
import { CssBaseline, ThemeProvider } from "@mui/material"
import Routes from "./Routes"
import theme from "./theme"
import { ApolloProvider } from "@apollo/client"
import client from "./client"

const App = () => (
  <div>
    <CssBaseline />
    <ThemeProvider theme={theme}>
      <ApolloProvider client={client}>
        <Routes />
      </ApolloProvider>
    </ThemeProvider>
  </div>
)

export default App
