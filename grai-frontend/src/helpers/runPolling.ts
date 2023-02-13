import { useEffect } from "react"

const useRunPolling = (
  status: string | undefined,
  startPolling: (interval: number) => void,
  stopPolling: () => void,
  interval: number = 1000
) =>
  useEffect(() => {
    switch (status) {
      case "queued":
      case "running":
        startPolling(interval)
        return

      case "success":
      case "error":
        stopPolling()
    }
  }, [status, startPolling, stopPolling, interval])

export default useRunPolling
