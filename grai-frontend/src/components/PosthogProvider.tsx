import React from "react"
import posthog from "posthog-js"
import { useLocation } from "react-router-dom"

const PosthogProvider: React.FC = () => {
  let location = useLocation()

  React.useEffect(() => {
    posthog.capture("$pageview")
  }, [location])

  return null
}

export default PosthogProvider
