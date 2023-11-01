/* istanbul ignore file */

declare global {
  interface Window {
    _hsq: any
  }
}

var hubspot: any = (window._hsq = window._hsq || [])

export default hubspot
