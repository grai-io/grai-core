import React, { ReactElement } from "react"

type BindHover = {
  onMouseEnter: () => void
  onMouseLeave: () => void
}

type HoverStateProps = {
  children: (
    hover: boolean,
    bindHover: BindHover,
    setHover: (hover: boolean) => void,
  ) => ReactElement<any, any> | null
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
