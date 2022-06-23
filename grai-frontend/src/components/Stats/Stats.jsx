import React from 'react'
import {
  Box,
  Heading, SimpleGrid,
  Text,
  useColorModeValue as mode
} from "@chakra-ui/react"

const statsData = [
    {
      label: "50%",
      subtext: "productivity increase"
    },
    {
      label: "5x",
      subtext: "faster development"
    },
    {
      label: "15",
      subtext: "minutes to debug distributed systems vs hours"
    },
    {
      label: "50%",
      subtext: "reduction in stream knowledge"
    }
]

const Stat = (props) => {
  const { stat }  = props
  return (
    <Box
      display={["flex"]}
      flexDirection={["column"]}
      alignItems={["center"]}
      marginBottom={["30px", "60px"]}
      color={mode("#2B2343", "cloud")}
    >
      <Heading
        marginBottom={["10px", "22px", "10px"]}
        fontSize={["40px", "55px", "40px", "70px", "90px"]}
      >
        {stat.label}
      </Heading>
      <Text
        fontSize={["12px", "16px", "14px", null, "16px"]}
        fontWeight={["500"]}
        textAlign={["center"]}
        px={["15px", "22px"]}
      >
        {stat.subtext}
      </Text>
    </Box>
  )
}

export const Stats = (props) => {
  return (
    <SimpleGrid
      as="section"
      columns={[2, null, 4]}
      bg={mode(
        "linear-gradient(180deg, #FFFFFE 0%, #FCF7EE 100%)",
        "linear-gradient(180deg, #382E57 0%, #584E68 100%)"
      )}
      {...props}
    >
      {statsData.map((stat, index) => (
        <Stat key={"Stats" + index} stat={stat} />
      ))}
    </SimpleGrid>
   
  )
}