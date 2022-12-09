import { ApolloProvider } from "@apollo/client"
import React, { ReactNode, useContext } from "react"
import client from "../client"
import AuthContext from "../components/auth/AuthContext"

type BackendProviderProps = {
  children: ReactNode
}

const BackendProvider: React.FC<BackendProviderProps> = ({ children }) => {
  const { authTokens, logoutUser } = useContext(AuthContext)

  return (
    <ApolloProvider client={client(authTokens?.access ?? "", logoutUser)}>
      {children}
    </ApolloProvider>
  )
}

export default BackendProvider
