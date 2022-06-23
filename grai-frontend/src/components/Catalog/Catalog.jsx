import React from 'react'
import {
  Box,
  Stack,
  Grid,
  GridItem,
  Flex,
  Heading,
  Circle,
  useColorModeValue as mode,
  Link,
  useMediaQuery,
  VStack,
  Image,
  HStack
} from "@chakra-ui/react"


export const items = [
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
  {
    title: 'Documentation',
    icon: 'https://github.com/dylan-profiler/visions/raw/develop/images/visions.png',
    description: "A simple, intuitive, and powerful tool for visualizing data.",
  },
]

export const AppItemHeader = (item) => {
  return (
    <Box bg="bastille">
      <HStack
        mx="10px"
      >
        <Box
          color="mango"
          fontSize="16px"         
        >
          {item.title}
        </Box>
        <Image
          borderRadius='full'
          boxSize='50px'
          src={item.icon}
        />
      </HStack>
    </Box>
  )
}

export const AppItemContent = (item) => {
  return (
    <Box>
      <VStack
        mx="10px"
        my="10px"
      >
        <Box
          color="mango"
          fontSize="16px"         
        >
          {item.description}
        </Box>
      </VStack>
    </Box>
  )
}

export const AppItem = (item) => {
  return (
    <Flex
    >
      <VStack
      >
        <AppItemHeader {...item}/>
        <AppItemContent {...item}/>
      </VStack>
    </Flex>
  )
}


export const AppGrid = (props) => {
  return (
    <Grid 
    templateColumns='repeat(3, 1fr)' 
    gap={6}
    >
      {items.map((item, idx) => {
        return (
          <GridItem>
            <AppItem key={idx} {...item} />
          </GridItem>
        )
      })}
    </Grid>
  )
}

export const Catalog = (props) => {
    const background = "linear-gradient(174.12deg, rgba(255, 255, 255, 0) 48.31%, rgba(245, 228, 234, 0.6006) 109.51%, #F1D7E0 193.01%)"
    return (
      <Flex
        bg={background}
        {...props}
      >
        <Flex
          my={"60px"}
          mx={"100px"}
          align="center"
          justify="center"
      
        >
          <AppGrid/>
        </Flex>
      </Flex>
    )
  }