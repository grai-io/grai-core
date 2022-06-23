import React from 'react'
import { ChakraProvider } from '@chakra-ui/react'
import Layout from './components/layout'
import theme from './@chakra-ui/gatsby-plugin/theme'

export const wrapPageElement = ({ element }) => {
  return (
    <ChakraProvider theme={theme} resetCSS>
      <Layout>{element}</Layout>
    </ChakraProvider>
  )
}
