import React from 'react'
import {
  Box,
  Heading,
  Grid,
  Text,
  useColorModeValue as mode,
} from "@chakra-ui/react"
import {Data} from './data'


export const IntegrationContainer = (props) => {
  return (
    <Box
      display={["flex"]}
      flexDirection={["column"]}
      alignItems={["center"]}
      justifyContent={["center"]}
      justifySelf={["center"]}
      borderRadius={["15px"]}
      w={["70px", "70px", null, "90px"]}
      h={["70px", "70px", null, "90px"]}
      {...props}
    >
      {props.children}
    </Box>
  )
}

export const IntegrationsSection = (props) => {
  const bg = mode("cloud", "web")
  return (
    <Box
      as="section"
      className={"integrations"}
      bg={bg}
      paddingTop={["0", "0", "0", "40px", "90px"]}
      {...props}
    >
      <Heading
        fontSize={["24px", "30px", null, "40px"]}
        fontWeight={["500"]}
        textAlign={["center"]}
        lineHeight={["36px"]}
        maxWidth={["275px", null, "500px", "750px"]}
        mx={["auto"]}
        marginBottom={[null, null, null, "30px"]}
        paddingTop={["45px", null, null, null, "0"]}
      >
        Integrates with your favorite tools
      </Heading>
      <Grid
        as={"section"}
        gridTemplateAreas={[
          `"int0 int1 int2 int3"
           "int4 int5 int6 int7"
           "int8 int9 int10 int11"
           "int12 int13 int14 int15"`,
          null,
          `"int0 int1 int2 int3 int4 int5 int6 int7 int8"
           ". int9 int10 int11 int12 int13 int14 int15 ."`
        ]}
        gridTemplateColumns={["repeat(4, 1fr)", null, "repeat(9, 1fr)"]}
        gridRowGap={["18px"]}
        gridColumnGap={["5px", "10px", "10px"]}
        alignContent={["center"]}
        justifyContent={["center"]}
        maxW={["350px", null, "680px", null, "1000px"]}
        mx={["auto"]}
        paddingTop={["30px"]}
        {...props}
        
      >
        {Data.integrations.map((integration, idx) => {
          return (
            <IntegrationContainer
              key={"IntegrationsSection" + idx}
              bg={integration.bg}
              gridArea={`int${idx}`}
            >
              {integration.icon}
              <Text
                fontWeight={["700"]}
                fontSize={["10px"]}
                textAlign={["center"]}
                margin={["0px"]}
                paddingTop={["5px"]}
                color="fontIllustration"
              >
                {integration.label}
              </Text>
            </IntegrationContainer>
          )
        })}
      </Grid>
    </Box>
  )
}