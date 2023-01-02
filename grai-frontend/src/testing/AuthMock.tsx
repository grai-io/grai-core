import AuthContext, { User } from "components/auth/AuthContext"
import React, { ReactNode } from "react"

type AuthMockProps = {
  user: User | null
  children: ReactNode
}

const AuthMock: React.FC<AuthMockProps> = ({ user, children }) => (
  <AuthContext.Provider
    value={{
      user,
      setUser: () => {},
      authTokens: null,
      setAuthTokens: () => {},
      registerUser: () => {},
      refresh: async () => {},
      loginUser: async () => new Promise(() => null),
      logoutUser: () => {},
    }}
  >
    {children}
  </AuthContext.Provider>
)

export default AuthMock
