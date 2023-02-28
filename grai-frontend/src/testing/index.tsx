/* istanbul ignore file */
import React, { ReactElement, ReactNode } from "react"
import { MockedResponse } from "@apollo/client/testing"
import { ThemeProvider } from "@mui/material"
import { render, RenderOptions } from "@testing-library/react"
import casual from "casual"
import { SnackbarProvider } from "notistack"
import { HelmetProvider } from "react-helmet-async"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import theme from "theme"
import GuestRoute from "components/auth/GuestRoute"
import WorkspaceProvider from "components/utils/WorkspaceProvider"
import AuthMock from "./AuthMock"
import AutoMockedProvider from "./AutoMockedProvider"

const mockResolvers = {
  Date: () => "2019-12-31",
  DateTime: () => "2019-07-24 11:14:37",
  PaginatorInfo: () => ({ currentPage: 1, total: 20 }),
  JSON: () => ({}),
  UUID: () => casual.uuid,
  Connection: () => ({
    name: "Connection 1",
  }),
  Node: () => ({
    metadata: {
      grai: {
        node_type: "Table",
      },
    },
  }),
}

type RouteType =
  | string
  | {
      path: string
      element: ReactNode
    }

type CustomRenderOptions = RenderOptions & {
  path?: string
  withRouter?: boolean
  route?: string | Partial<Location>
  routes?: RouteType[]
  initialEntries?: (string | Partial<Location>)[] | null
  loggedIn?: boolean
  guestRoute?: boolean
  mocks?: readonly MockedResponse<Record<string, any>>[]
}

const customRender = (ui: ReactElement, options?: CustomRenderOptions) => {
  if (options?.withRouter || options?.path || options?.route || options?.routes)
    return renderWithRouter(ui, options)

  return basicRender(ui, options)
}

const basicRender = (
  ui: ReactElement,
  { loggedIn = true, mocks }: CustomRenderOptions = {}
) =>
  render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <SnackbarProvider>
          <ThemeProvider theme={theme}>
            <AuthMock initialLoggedIn={loggedIn}>
              <AutoMockedProvider mockResolvers={mockResolvers} mocks={mocks}>
                {props.children}
              </AutoMockedProvider>
            </AuthMock>
          </ThemeProvider>
        </SnackbarProvider>
      </HelmetProvider>
    ),
  })

const renderWithRouter = (
  ui: ReactElement,
  {
    path = "/",
    route = "/",
    routes = [],
    initialEntries = null,
    loggedIn = true,
    guestRoute = false,
    mocks,
  }: CustomRenderOptions = {}
) => {
  return render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <ThemeProvider theme={theme}>
          <AutoMockedProvider mockResolvers={mockResolvers} mocks={mocks}>
            <MemoryRouter initialEntries={initialEntries ?? [route]}>
              <AuthMock initialLoggedIn={loggedIn}>
                <SnackbarProvider maxSnack={3} hideIconVariant>
                  <Routes>
                    <Route element={<WorkspaceProvider />}>
                      {guestRoute ? (
                        <Route element={<GuestRoute />}>
                          <Route path={path} element={props.children} />
                        </Route>
                      ) : (
                        <Route path={path} element={props.children} />
                      )}
                      {routes.map(route =>
                        typeof route === "string" ? (
                          <Route
                            key={route}
                            path={route}
                            element={<>New Page</>}
                          />
                        ) : (
                          <Route
                            key={route.path}
                            path={route.path}
                            element={route.element}
                          />
                        )
                      )}
                    </Route>
                  </Routes>
                </SnackbarProvider>
              </AuthMock>
            </MemoryRouter>
          </AutoMockedProvider>
        </ThemeProvider>
      </HelmetProvider>
    ),
  })
}

export * from "@testing-library/react"
export { customRender as render }
