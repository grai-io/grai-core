const runPolling =
  (
    status: string | undefined,
    startPolling: (interval: number) => void,
    stopPolling: () => void,
    interval: number = 1000
  ) =>
  () => {
    switch (status) {
      case "queued":
      case "running":
        startPolling(interval)
        return

      case "success":
      case "error":
        stopPolling()
    }
  }

export default runPolling
