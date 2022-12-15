/* istanbul ignore file */
import React, { ReactElement, ReactNode } from "react"
import { MockedProvider, MockedResponse } from "@apollo/client/testing"
import { ThemeProvider } from "@mui/material"
import { render, RenderOptions } from "@testing-library/react"
import { SnackbarProvider } from "notistack"
import { HelmetProvider } from "react-helmet-async"
import { MemoryRouter, Route, Routes } from "react-router-dom"
import theme from "theme"
import AutoMockedProvider from "./AutoMockedProvider"
import AuthContext, { AuthProvider } from "components/auth/AuthContext"

const mockResolvers = {
  Date: () => "2019-12-31",
  DateTime: () => "2019-07-24 11:14:37",
  PaginatorInfo: () => ({ currentPage: 1, total: 20 }),
  JSON: () => ({}),
}

const customRender = (ui: ReactElement, options?: RenderOptions) =>
  render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <SnackbarProvider>
          <ThemeProvider theme={theme}>
            <AuthProvider>
              <AutoMockedProvider mockResolvers={mockResolvers}>
                {props.children}
              </AutoMockedProvider>
            </AuthProvider>
          </ThemeProvider>
        </SnackbarProvider>
      </HelmetProvider>
    ),
    ...options,
  })

type RouteType =
  | string
  | {
      path: string
      element: ReactNode
    }

export const renderWithRouter = (
  ui: ReactElement,
  {
    path = "/",
    route = "/",
    routes = [],
    initialEntries = null,
  }: {
    path?: string
    route?: string
    routes?: RouteType[]
    initialEntries?: string[] | null
  } = {}
) => {
  return render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <ThemeProvider theme={theme}>
          <AutoMockedProvider mockResolvers={mockResolvers}>
            <MemoryRouter initialEntries={initialEntries ?? [route]}>
              <AuthContext.Provider
                value={{
                  user: {
                    id: "1",
                    name: "user1",
                    email: "user@example.com",
                  },
                  setUser: () => {},
                  authTokens: null,
                  setAuthTokens: () => {},
                  registerUser: () => {},
                  refresh: async () => {},
                  loginUser: async () => new Promise(() => null),
                  logoutUser: () => {},
                }}
              >
                <SnackbarProvider maxSnack={3} hideIconVariant>
                  <Routes>
                    <Route path={path} element={props.children} />
                    {routes.map(route =>
                      typeof route === "string" ? (
                        <Route key={route} path={route} element={<></>} />
                      ) : (
                        <Route
                          key={route.path}
                          path={route.path}
                          element={route.element}
                        />
                      )
                    )}
                  </Routes>
                </SnackbarProvider>
              </AuthContext.Provider>
            </MemoryRouter>
          </AutoMockedProvider>
        </ThemeProvider>
      </HelmetProvider>
    ),
  })
}

export const renderWithMocks = (
  ui: ReactElement,
  mocks: readonly MockedResponse<Record<string, any>>[],
  {
    path = "/",
    route = "/",
    routes = [],
  }: {
    path?: string
    route?: string
    routes?: string[]
  } = {}
) => {
  return render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <ThemeProvider theme={theme}>
          <MockedProvider mocks={mocks} addTypename={false}>
            <MemoryRouter initialEntries={[route]}>
              <AuthContext.Provider
                value={{
                  user: {
                    id: "1",
                    name: "user1",
                    email: "user@example.com",
                  },
                  setUser: () => {},
                  authTokens: null,
                  setAuthTokens: () => {},
                  registerUser: () => {},
                  refresh: async () => {},
                  loginUser: async () => new Promise(() => null),
                  logoutUser: () => {},
                }}
              >
                <SnackbarProvider maxSnack={3} hideIconVariant>
                  <Routes>
                    <Route path={path} element={props.children} />
                    {routes.map(path => (
                      <Route key={path} path={path} element={<></>} />
                    ))}
                  </Routes>
                </SnackbarProvider>
              </AuthContext.Provider>
            </MemoryRouter>
          </MockedProvider>
        </ThemeProvider>
      </HelmetProvider>
    ),
  })
}

export * from "@testing-library/react"
export { customRender as render }
