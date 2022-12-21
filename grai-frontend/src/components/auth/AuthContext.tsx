import { createContext, useState, useEffect, ReactNode } from "react"
import jwt_decode from "jwt-decode"
declare global {
  interface Window {
    _env_: any
  }
}

export type User = {}

export type Tokens = {
  access: string
  refresh: string
}

type AuthContextType = {
  user: User | null
  setUser: (user: User | null) => void
  authTokens: Tokens | null
  setAuthTokens: (tokens: Tokens | null) => void
  registerUser: (username: string, password: string, password2: string) => void
  refresh: () => Promise<void>
  loginUser: (username: string, password: string) => Promise<void>
  logoutUser: () => void
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  setUser: () => {},
  authTokens: null,
  setAuthTokens: () => {},
  registerUser: () => {},
  refresh: async () => {},
  loginUser: async () => new Promise(() => null),
  logoutUser: () => {},
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
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens") ?? "")
      : null
  )
  const [user, setUser] = useState<User | null>(() =>
    localStorage.getItem("authTokens")
      ? jwt_decode(localStorage.getItem("authTokens") ?? "")
      : null
  )
  const [loading, setLoading] = useState(true)

  // const navigate = useNavigate()

  const loginUser = async (username: string, password: string) => {
    const response = await fetch(
      `${baseURL}/api/v1/auth/jwttoken/`.replace(/([^:])(\/\/+)/g, "$1/"),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          password,
        }),
      }
    )
    const data = await response.json()

    if (response.status === 200) {
      setAuthTokens(data)
      setUser(jwt_decode(data.access))
      localStorage.setItem("authTokens", JSON.stringify(data))
    } else {
      alert("Something went wrong!")
    }
  }

  const refresh = async () => {
    const response = await fetch(
      `${baseURL}/api/v1/auth/jwttoken/refresh/`.replace(
        /([^:])(\/\/+)/g,
        "$1/"
      ),
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          refresh: authTokens?.refresh,
        }),
      }
    ).catch(error => {
      if (error.response.status === 401) {
        return
      }

      throw error
    })

    if (!response) return

    const data = await response.json()

    if (response.status === 200) {
      const updatedAuthTokens: Tokens = authTokens
        ? { refresh: authTokens.refresh, access: data.access }
        : { access: data.access, refresh: "" }

      localStorage.setItem("authTokens", JSON.stringify(updatedAuthTokens))

      setAuthTokens(updatedAuthTokens)
      setUser(jwt_decode(data.access))
    } else {
      if (response.status === 401) {
        setAuthTokens(null)
        setUser(null)

        return
      }

      alert("Something went wrong!")
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
    setAuthTokens(null)
    setUser(null)
    localStorage.removeItem("authTokens")
    // navigate("/")
  }

  const contextData = {
    user,
    setUser,
    authTokens,
    setAuthTokens,
    registerUser,
    refresh,
    loginUser,
    logoutUser,
  }

  useEffect(() => {
    if (authTokens) {
      setUser(jwt_decode(authTokens.access))
    }
    setLoading(false)
  }, [authTokens, loading])

  return (
    <AuthContext.Provider value={contextData}>
      {loading ? null : children}
    </AuthContext.Provider>
  )
}
