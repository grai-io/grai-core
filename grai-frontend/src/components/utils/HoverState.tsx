import React from "react"

type BindHover = {
  onMouseEnter: () => void
  onMouseLeave: () => void
}

type HoverStateProps = {
  children: (
    hover: boolean,
    bindHover: BindHover,
    setHover: (hover: boolean) => void,
  ) => React.ReactNode
}

const HoverState: React.FC<HoverStateProps> = ({ children }) => {
  const [hover, setHover] = React.useState(false)

  const bindHover = {
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
  }

  return children(hover, bindHover, setHover)
}

export default HoverState
