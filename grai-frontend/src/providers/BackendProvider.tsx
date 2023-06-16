import React, { ReactNode } from "react"
import { ApolloProvider } from "@apollo/client"
import useLocalStorage from "helpers/useLocalStorage"
import { AuthProvider } from "components/auth/AuthContext"
import make_client from "client"

type BackendProviderProps = {
  children: ReactNode
}

const BackendProvider: React.FC<BackendProviderProps> = ({ children }) => {
  const [loggedIn, setLoggedIn] = useLocalStorage("loggedIn", false)

  const logoutUser = () => setLoggedIn(false)

  const client = make_client(logoutUser)

  return (
    <ApolloProvider client={client}>
      <AuthProvider
        loggedIn={loggedIn}
        setLoggedIn={setLoggedIn}
        client={client}
      >
        {children}
      </AuthProvider>
    </ApolloProvider>
  )
}

export default BackendProvider
