/* istanbul ignore file */
import posthog, { Properties } from "posthog-js"

export const posthogApiKey =
  window._env_?.REACT_APP_POSTHOG_API_KEY ??
  process.env.REACT_APP_POSTHOG_API_KEY

const posthogHost =
  window._env_?.REACT_APP_POSTHOG_HOST ??
  process.env.REACT_APP_POSTHOG_HOST ??
  "https://app.posthog.com"

if (posthogApiKey)
  posthog.init(posthogApiKey, {
    api_host: posthogHost,
  })

const resPosthog = posthog

resPosthog.identify = (
  new_distinct_id?: string | undefined,
  userPropertiesToSet?: Properties | undefined,
  userPropertiesToSetOnce?: Properties | undefined
) =>
  posthogApiKey &&
  posthog.identify(
    new_distinct_id,
    userPropertiesToSet,
    userPropertiesToSetOnce
  )

resPosthog.reset = (reset_device_id?: boolean | undefined) =>
  posthogApiKey && posthog.reset(reset_device_id)

export default resPosthog
