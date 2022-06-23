import React from 'react'
import {
  Box,
  Flex,
} from '@chakra-ui/react'
import { BenefitsData } from "./Data"

export const Benefit = (benefit, props) => {
  const marginX = {base: "25px", md: "75px"}
  return (
    <Flex
      bg={benefit.bg}
      paddingTop={{base: "60px", md: "73px"}}
      paddingBottom={{base: "84px", md: "105px"}}
      direction={{base: "column", md: benefit.rowOrder}}
      align={"space-evenly"}
    >
      <Flex
        w={{base: "100%", md: "50%"}}
        justify={"center"}
        align={"center"}
        marginBottom={{base: "27px", md: null}}
        paddingX={marginX}
      >
        {benefit.icon}
      </Flex>
      
      <Flex
        w={{base: "100%", md: "50%"}}
        align={"center"}
        justify={"center"}
        alignItems={"flex-start"}
        direction={["column"]}
        paddingX={marginX}
      >
        <Box
          fontFamily={"body"}
          fontWeight={"700"}
          fontSize={{base: "14px", md: "18px"}}
          lineHeight={"130%"}
          letterSpacing={"10%"}
          color={benefit.textColor}
          marginBottom={{base: "24px"}}
        >
          {benefit.label}
        </Box>
        <Box
          fontFamily={"heading"}
          fontWeight={"700"}
          fontSize={{base: "34px", md: "48px"}}
          lineHeight={"124%"}
          letterSpacing={"10%"}
          color={benefit.textColor}
          marginBottom={{base: "26px"}}
        >
          {benefit.header}
        </Box>
        <Box
          fontFamily={"body"}
          fontWeight={"500"}
          fontSize={{base: "14px", md: "18px"}}
          lineHeight={"130%"}
          color={benefit.textColor}
        >
          {benefit.text}
        </Box>
        </Flex>
    </Flex>
  )
}

export const BenefitsContainer = (props) => {
  return (
    BenefitsData.map((benefit, idx) => {
      benefit.rowOrder = idx % 2 === 0 ? "row" : "row-reverse"
      return (
        <Benefit
          key={"BenefitsContainer" + idx}
          {...benefit}
        >
        </Benefit>
      )
    })
  )
}
export const BenefitsSection = (props) => {
  return (
    <Box
      as='section'
      // {...props}
      // bg={mode('cloud', '#372D56')}
      // paddingTop={["50px"]}
    >
      <BenefitsContainer />
    </Box>
  )
}