import React, { Component, ErrorInfo, ReactNode } from "react"
import { Alert, AlertTitle } from "@mui/material"

interface Props {
  children?: ReactNode
}

interface State {
  hasError: boolean
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  public static getDerivedStateFromError(_: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <Alert severity="error">
          <AlertTitle>Error!</AlertTitle>
          Sorry there was an error
        </Alert>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
