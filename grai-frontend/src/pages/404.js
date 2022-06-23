import * as React from "react"
import {
  Box,
  Stack,
  Flex,
  Heading,
  Circle,
  useColorModeValue as mode,
  Link,
  useMediaQuery
} from "@chakra-ui/react"
import Layout from "../components/layout"
import Seo from "../components/seo"

const NotFoundPage = () => (

  <>
    <Seo title="404: Not found" />
    <Flex
      align={"center"}
      justify={"center"}
      bg="linear-gradient(176.94deg, rgba(255, 255, 255, 0) -10.62%, rgba(255, 223, 189, 0.11913) 51.22%, rgba(255, 193, 127, 0.24168) 114.84%, rgba(255, 181, 103, 0.3) 145.12%)"
      height={{base: "500px"}}
    >
      <Stack
        align={"center"}
      >
        <Heading
          color={'bastille'}
        >404: Not Found</Heading>
        <Heading>Oh, drat these computers. They’re so naughty and so complex. I could pinch them.</Heading>
      </Stack>
    </Flex>

  </>
)

export default NotFoundPage