import React from "react"
import posthog from "posthog-js"
import { useLocation } from "react-router-dom"
import hubspot from "hubspot"

const PosthogProvider: React.FC = () => {
  const location = useLocation()

  React.useEffect(() => {
    posthog.capture("$pageview")
    hubspot.push(["setPath", location.pathname + location.search])
    hubspot.push(["trackPageView"])
  }, [location])

  return null
}

export default PosthogProvider
