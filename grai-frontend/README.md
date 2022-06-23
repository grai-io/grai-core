# Getting Started

All of the components in Chakra UI are designed for Chakra UI v1.0+<br>

#In some components we use `react-icons` to pep up the visual appearance. Feel free to replace them with your own icons.

## Installation

Inside your React project directory, install Chakra UI by running either of the following:

```sh
# npm
$ npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion react-icons
```

or when using yarn:

```sh
# yarn
yarn add @chakra-ui/react @emotion/react @emotion/styled framer-motion react-icons
```

## Setup Chakra UI

For Chakra UI to work correctly, you need to setup the ChakraProvider at the root of your application.

```tsx
import * as React from 'react'
import { ChakraProvider } from '@chakra-ui/react'

export const App = () => {
  return (
    <ChakraProvider>
      <App />
    </ChakraProvider>
  )
}
```

## Chakra UI Docs

If you need more help, feel free to visit the [official website](https://chakra-ui.com) of Chakra UI. Here you can find help with installation, theming and much more.
