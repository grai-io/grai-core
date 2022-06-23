import * as React from 'react'
import { ChakraProvider } from '@chakra-ui/react'

import theme from '../src/theme';

export const App = ({Component, pageProps}) => {
  return (
    <ChakraProvider theme={theme}>
      <Component {...pageProps}/>
       {/* <App /> */}
    </ChakraProvider>
  )
}