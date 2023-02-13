/* istanbul ignore file */
import { ApolloClient, gql, NormalizedCacheObject } from "@apollo/client"
import { createContext, ReactNode } from "react"
import { Login, LoginVariables } from "./__generated__/Login"
import { Logout } from "./__generated__/Logout"
import { Register, RegisterVariables } from "./__generated__/Register"

export const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      id
      username
      first_name
      last_name
    }
  }
`

export const LOGOUT = gql`
  mutation Logout {
    logout
  }
`

export const REGISTER = gql`
  mutation Register($username: String!, $password: String!) {
    register(username: $username, password: $password) {
      id
      username
      first_name
      last_name
    }
  }
`

type AuthContextType = {
  registerUser: (username: string, password: string) => void
  loginUser: (username: string, password: string) => Promise<void>
  logoutUser: () => void
  loggedIn: boolean
}

const AuthContext = createContext<AuthContextType>({
  registerUser: () => {},
  loginUser: async () => new Promise(() => null),
  logoutUser: () => {},
  loggedIn: false,
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
  const loginUser = async (username: string, password: string) =>
    client
      .mutate<Login, LoginVariables>({
        mutation: LOGIN,
        variables: {
          username,
          password,
        },
      })
      .then(() => setLoggedIn(true))

  const registerUser = async (username: string, password: string) =>
    client
      .mutate<Register, RegisterVariables>({
        mutation: REGISTER,
        variables: {
          username,
          password,
        },
      })
      .then(() => setLoggedIn(true))

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
    registerUser,
    loginUser,
    logoutUser,
    loggedIn,
  }

  return (
    <AuthContext.Provider value={contextData}>{children}</AuthContext.Provider>
  )
}
