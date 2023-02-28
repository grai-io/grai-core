/* istanbul ignore file */
import React, { ReactNode, useState } from "react"
import AuthContext from "components/auth/AuthContext"

type AuthMockProps = {
  initialLoggedIn: boolean
  children: ReactNode
}

const AuthMock: React.FC<AuthMockProps> = ({ children, initialLoggedIn }) => {
  const [loggedIn, setLoggedIn] = useState(initialLoggedIn)

  return (
    <AuthContext.Provider
      value={{
        logoutUser: () => {
          setLoggedIn(false)
        },
        loggedIn,
        setLoggedIn,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export default AuthMock
