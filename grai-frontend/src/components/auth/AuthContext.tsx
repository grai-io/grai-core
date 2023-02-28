/* istanbul ignore file */
import { createContext, ReactNode } from "react"
import { ApolloClient, gql, NormalizedCacheObject } from "@apollo/client"
import { Logout } from "./__generated__/Logout"

export const LOGOUT = gql`
  mutation Logout {
    logout
  }
`

type AuthContextType = {
  logoutUser: () => void
  loggedIn: boolean
  setLoggedIn: (loggedIn: boolean) => void
}

const AuthContext = createContext<AuthContextType>({
  logoutUser: () => {},
  loggedIn: false,
  setLoggedIn: () => {},
})

export default AuthContext

type AuthProviderProps = {
  loggedIn: boolean
  setLoggedIn: (value: boolean) => void
  client: ApolloClient<NormalizedCacheObject>
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({
  loggedIn,
  setLoggedIn,
  client,
  children,
}) => {
  const logoutUser = async () =>
    client
      .mutate<Logout>({
        mutation: LOGOUT,
      })
      .then(() => {
        client.resetStore()
        setLoggedIn(false)
      })

  const contextData = {
    logoutUser,
    loggedIn,
    setLoggedIn,
  }

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  )
}
