import { ApolloProvider } from "@apollo/client"
import React, { ReactNode, useContext } from "react"
import AuthContext from "components/auth/AuthContext"
import client from "client"

type BackendProviderProps = {
  children: ReactNode
}

const BackendProvider: React.FC<BackendProviderProps> = ({ children }) => {
  const { authTokens, refresh } = useContext(AuthContext)

  return (
    <ApolloProvider client={client(authTokens, refresh)}>
      {children}
    </ApolloProvider>
  )
}

export default BackendProvider
