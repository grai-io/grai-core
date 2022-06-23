import * as React from 'react'
import { MotionBox } from './MotionBox'

// const bg = "linear-gradient(176.94deg, rgba(255, 255, 255, 0) -10.62%, rgba(255, 223, 189, 0.3971) 51.22%, rgba(255, 193, 127, 0.8056) 114.84%, #FFB567 145.12%)"
const bg = "bastille"
export const NavMenu = React.forwardRef((props, ref) => (
  <MotionBox
    {...props}
    ref={ref}
    initial="init"
    variants={variants}
    outline="0"
    opacity="0"
    bg={bg}
    w="full"
    h="100vh"
    // pos="absolute"
    insetX="0"
    align={["center"]}
    justify={["center"]}
  />
))

NavMenu.displayName = 'NavMenu'

const variants = {
  init: {
    opacity: 0,
    y: -4,
    display: 'none',
    transition: {
      duration: 0,
    },
  },
  open: {
    opacity: 1,
    y: 0,
    display: 'block',
    transition: {
      duration: 0.15,
    },
  },
  closed: {
    opacity: 0,
    y: -4,
    transition: {
      duration: 0.1,
    },
    transitionEnd: {
      display: 'none',
    },
  },
}