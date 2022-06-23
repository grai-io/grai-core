import { chakra, useToken } from '@chakra-ui/react'
import * as React from 'react'

export const Logo = (props) => {
  // use colorScheme to change from darkmode to light
  const { iconColor = 'currentColor', ...rest } = props
  const color = useToken('colors', iconColor)
  return (
    <chakra.svg viewBox="0 0 19 12" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path
        fillRule="evenodd"
        clipRule="evenodd"
        d="M0.993652 2V0H18.9937V2H0.993652ZM0.993652 7H18.9937V5H0.993652V7ZM0.993652 12H18.9937V10H0.993652V12Z" fill="white"/>
    </chakra.svg>
  )
}





