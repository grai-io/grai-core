import { Outlet, Navigate } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "./AuthContext"

const PrivateRoute: React.FC = () => {
  const { user } = useContext(AuthContext)

  if (!user) return <Navigate to="/login" />

  return <Outlet />
}

export default PrivateRoute
