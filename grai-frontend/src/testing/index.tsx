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
import casual from "casual"
import AuthMock from "./AuthMock"

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
      node_type: "Table",
    },
  }),
}

const defaultUser = {
  id: "1",
  name: "user1",
  email: "user@example.com",
}

const customRender = (ui: ReactElement, options?: RenderOptions) =>
  render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <SnackbarProvider>
          <ThemeProvider theme={theme}>
            <AuthMock user={defaultUser}>
              <AutoMockedProvider mockResolvers={mockResolvers}>
                {props.children}
              </AutoMockedProvider>
            </AuthMock>
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
    user = {
      id: "1",
      name: "user1",
      email: "user@example.com",
    },
  }: {
    path?: string
    route?: string
    routes?: RouteType[]
    initialEntries?: string[] | null
    user?: any
  } = {}
) => {
  return render(ui, {
    wrapper: props => (
      <HelmetProvider>
        <ThemeProvider theme={theme}>
          <AutoMockedProvider mockResolvers={mockResolvers}>
            <MemoryRouter initialEntries={initialEntries ?? [route]}>
              <AuthMock user={user}>
                <SnackbarProvider maxSnack={3} hideIconVariant>
                  <Routes>
                    <Route path={path} element={props.children} />
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
              <AuthMock user={defaultUser}>
                <SnackbarProvider maxSnack={3} hideIconVariant>
                  <Routes>
                    <Route path={path} element={props.children} />
                    {routes.map(path => (
                      <Route key={path} path={path} element={<>New Page</>} />
                    ))}
                  </Routes>
                </SnackbarProvider>
              </AuthMock>
            </MemoryRouter>
          </MockedProvider>
        </ThemeProvider>
      </HelmetProvider>
    ),
  })
}

export * from "@testing-library/react"
export { customRender as render }
