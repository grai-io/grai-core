import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material"
import React, { useContext } from "react"
import { Link } from "react-router-dom"
import AuthContext from "../auth/AuthContext"

const AppTopBar: React.FC = () => {
  const { logoutUser } = useContext(AuthContext)

  const handleLogout = () => logoutUser()

  return (
    <AppBar position="static">
      <Toolbar>
        <Box component={Link} to="/" sx={{ mt: 1 }}>
          <svg
            width="105"
            height="43"
            viewBox="0 0 1401 566"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M499.963 271.925C473.116 268.223 451.825 246.941 448.122 220.106L442.567 179.623H440.716L401.835 174.302C374.988 170.601 353.697 149.318 349.994 122.483L344.671 82H333.793L328.239 122.483C324.536 149.318 303.244 170.601 276.398 174.302L237.517 179.623H235.897L230.342 220.106C226.639 246.941 205.347 268.223 178.501 271.925L138 277.477V288.349L178.501 293.901C205.347 297.603 226.639 318.885 230.342 345.72L235.897 386.203H236.822L276.166 391.755C303.012 395.457 324.304 416.739 328.007 443.574L333.562 484.057H344.439L349.994 443.574C353.697 416.739 374.988 395.457 401.835 391.755L441.179 386.203H442.336L447.89 345.72C451.593 318.885 472.885 297.603 499.731 293.901L540.232 288.349V277.477L499.963 271.925ZM402.066 196.51L429.838 192.577L425.904 220.106C422.201 246.941 400.909 268.223 374.063 271.925L346.291 275.857L350.225 248.329C353.928 221.263 375.22 200.211 402.066 196.51ZM328.007 248.097L331.942 275.626L304.17 271.693C277.323 267.992 256.031 246.709 252.328 219.875L248.394 192.346L276.166 196.279C303.012 200.211 324.304 221.263 328.007 248.097ZM276.166 369.547L248.394 373.48L252.328 345.951C256.031 319.117 277.323 297.834 304.17 294.133L331.942 290.2L328.007 317.729C324.304 344.563 303.012 365.846 276.166 369.547ZM350.225 317.729L346.291 290.2L374.063 294.133C400.909 297.834 422.201 319.117 425.904 345.951L429.838 373.48L402.066 369.547C375.22 365.846 353.928 344.563 350.225 317.729Z"
              fill="#FFB567"
            />
            <path
              d="M760.012 206.193C785.488 206.193 808.254 217.571 814.487 243.307H870.86C865.169 190.209 820.179 155.804 761.367 155.804C685.48 155.804 635.883 209.173 635.883 283.13C635.883 358.442 684.125 408.83 752.694 408.83C781.965 408.83 808.525 398.536 821.805 383.094L824.786 405.308H870.86V264.437H755.404V311.575H820.45C818.011 337.04 800.123 358.983 759.741 358.983C720.713 358.983 692.798 334.331 692.798 285.026C692.527 237.347 715.564 206.193 760.012 206.193Z"
              fill="#FFB567"
            />
            <path
              d="M1016.4 239.244C1009.36 237.618 1002.85 236.805 996.888 236.805C974.664 236.805 960.029 247.642 952.982 263.896L950.272 239.244H902.301V404.767H953.524V332.706C953.524 299.926 971.141 286.923 1000.41 286.923H1016.67V239.244H1016.4Z"
              fill="#FFB567"
            />
            <path
              d="M1079.28 409.372C1104.21 409.372 1126.16 398.535 1131.31 383.094L1134.57 405.037H1179.56V308.324C1179.56 260.915 1152.45 234.096 1104.21 234.096C1056.78 234.096 1025.89 258.748 1025.89 296.133H1068.44C1068.44 281.233 1080.09 272.835 1101.5 272.835C1119.66 272.835 1129.69 281.504 1129.69 297.759V300.468L1083.34 303.989C1043.5 306.969 1022.09 325.933 1022.09 356.274C1022.09 388.783 1044.04 409.372 1079.28 409.372ZM1097.17 371.716C1081.45 371.716 1074.4 366.027 1074.4 354.107C1074.4 343.542 1082.26 338.394 1104.48 336.498L1130.23 334.06V343C1130.23 361.963 1116.68 371.716 1097.17 371.716Z"
              fill="#FFB567"
            />
            <path
              d="M1234.85 213.507C1250.84 213.507 1263.85 200.503 1263.85 184.249C1263.85 167.995 1250.84 155.262 1234.85 155.262C1218.59 155.262 1205.58 167.995 1205.58 184.249C1205.85 200.503 1218.59 213.507 1234.85 213.507ZM1209.64 405.037H1260.86V239.243H1209.64V405.037Z"
              fill="#FFB567"
            />
          </svg>
        </Box>
        <Button component={Link} to="/graph" sx={{ my: 2, color: "inherit" }}>
          Graph
        </Button>
        <Button component={Link} to="/nodes" sx={{ my: 2, color: "inherit" }}>
          Nodes
        </Button>
        <Button component={Link} to="/edges" sx={{ my: 2, color: "inherit" }}>
          Edges
        </Button>
        <Button
          component={Link}
          to="/connections"
          sx={{ my: 2, color: "inherit" }}
        >
          Connections
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        <Button color="inherit" onClick={handleLogout}>
          Logout
        </Button>
      </Toolbar>
    </AppBar>
  )
}

export default AppTopBar
