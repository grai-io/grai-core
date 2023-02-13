import { Outlet, Navigate, useLocation } from "react-router-dom"
import { useContext } from "react"
import AuthContext from "./AuthContext"

const PrivateRoute: React.FC = () => {
  const { loggedIn } = useContext(AuthContext)
  let location = useLocation()

  if (!loggedIn) return <Navigate to="/login" state={{ redirect: location }} />

  return <Outlet />
}

export default PrivateRoute
