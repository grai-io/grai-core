/* istanbul ignore file */
import AuthContext from "components/auth/AuthContext"
import React, { ReactNode, useState } from "react"

type AuthMockProps = {
  initialLoggedIn: boolean
  throwError?: boolean
  children: ReactNode
}

const AuthMock: React.FC<AuthMockProps> = ({
  children,
  initialLoggedIn,
  throwError,
}) => {
  const [loggedIn, setLoggedIn] = useState(initialLoggedIn)

  return (
    <AuthContext.Provider
      value={{
        registerUser: () => {
          setLoggedIn(true)
        },
        loginUser: async () => {
          if (throwError) throw Error("Login Error")

          setLoggedIn(true)
          return new Promise(() => null)
        },
        logoutUser: () => {
          setLoggedIn(false)
        },
        loggedIn,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthMock
