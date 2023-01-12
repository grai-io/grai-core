/* istanbul ignore file */
import { createContext, ReactNode } from "react"
import useLocalStorage from "helpers/useLocalStorage"
declare global {
  interface Window {
    _env_: any
  }
}

export type User = {}

type AuthContextType = {
  registerUser: (username: string, password: string, password2: string) => void
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

const baseURL =
  window._env_?.REACT_APP_SERVER_URL ??
  process.env.REACT_APP_SERVER_URL ??
  "http://localhost:8000"

type AuthProviderProps = {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [loggedIn, setLoggedIn] = useLocalStorage("loggedIn", false)

  const loginUser = async (username: string, password: string) => {
    const response = await fetch(
      `${baseURL}/login/`.replace(/([^:])(\/\/+)/g, "$1/"),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
        credentials: "include",
      }
    )

    if (response.status === 200) {
      setLoggedIn(true)
    } else if (response.status === 401) {
      throw new Error("Incorrect password")
    } else {
      throw new Error("Error")
    }
  }

  const registerUser = async (
    username: string,
    password: string,
    password2: string
  ) => {
    const response = await fetch(
      `${baseURL}/api/register/`.replace(/([^:])(\/\/+)/g, "$1/"),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
          password2,
        }),
      }
    )
    if (response.status !== 201) alert("Something went wrong!")
  }

  const logoutUser = () => {
    setLoggedIn(false)
  }

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
