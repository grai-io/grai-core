import { Outlet, Navigate, useLocation } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "./AuthContext"

const PrivateRoute: React.FC = () => {
  const { user } = useContext(AuthContext)
  let location = useLocation()

  if (!user) return <Navigate to="/login" state={{ redirect: location }} />

  return <Outlet />
}

export default PrivateRoute
