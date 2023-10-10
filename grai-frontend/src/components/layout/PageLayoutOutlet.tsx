import React from "react"
import { Outlet } from "react-router-dom"
import PageLayout from "./PageLayout"

const PageLayoutOutlet: React.FC = () => (
  <PageLayout>
    <Outlet />
  </PageLayout>
)

export default PageLayoutOutlet
