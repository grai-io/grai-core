import React from 'react'
import {
    Flex,
    Button,
    SimpleGrid,
    GridItem,
    FormLabel,
    FormControl,
    FormErrorMessage,
    Input,
    Link
  } from '@chakra-ui/react'
import { Formik, Field, Form} from 'formik';
import {SignUpAPI} from '../../Auth'

function required(fieldName) {
  return function(value) {
    let error
    if (!value) {
      error = [fieldName, 'is required'].join(' ')
    }
    console.log(error)
    return error
  }
}

function validateEmail(value){
  let error
  var re = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/
  error = required("Email Address")(value)
  if (!value){
    return error
  } else if (!re.test(value)) {
    error = 'Invalid email address.'
  }

  return error
}

function validatePhoneNumber(value){
  let error
  var re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im
  if (value && !re.test(value)) {
    error = 'Invalid phone number.'
  }

  return error
} 

export const fields = [
  {
    id: "firstName",
    placeholder: "Tommy",
    text: "First Name",
    required: true,
    validator: required("First Name"),
  },
  {
    id: "lastName",
    placeholder: "Tutone",
    text: "Last Name",
    required: true,
    validator: required("Last Name"),
  },
  {
    id: "companyName",
    placeholder: "Columbia Records",
    text: "Company Name",
    required: true,
    validator: required("Company Name"),
    colSpan: 4,
  },
  {
    id: "emailAddress",
    placeholder: "jenny@yonumba.com",
    text: "Email Address",
    required: true,
    validator: validateEmail,

  },
  {
    id: "phoneNumber",
    placeholder: '+1 (314) 867-5309',
    text: "Phone Number",
    validator: validatePhoneNumber,
  },
]


export const SignupBase = (props) => {
  let initialValues = Object.assign({}, ...fields.map((x) => ({[x.id]: ''})))
  initialValues.location = props.location
  const gridWidths = {base: 4, lg: 2}
  const baseStyle = {
    color: {base: "bastille"},
    fontFamily: "heading",
    fontSize: {base: "16px", lg: "15px"},
    fontWeight: "500",
    lineHeight: "135%"
  }
  return (
    <Formik
      initialValues={initialValues}
      validateOnChange={false}
      onSubmit={(values, actions) => {
        //console.log(values)
        //SignUpAPI(values)
        SignUpAPI(values)
        .then(result => {
          actions.setSubmitting(false)
          alert("thank you, you're all set!")
          actions.resetForm()
        })
        .catch((error) => {
          actions.setSubmitting(false)
          alert(`Apologies, we encountered the following error: ${error}`)
        })

      }}
    >
      {(props) => (
        <Form>
          <SimpleGrid 
            columns={4}
            columnGap={{base: "0 auto", lg: "26px"}}
            rowGap={{base: "32px", lg: "32px"}}
          >
              {fields.map((formfield, idx) => {
                return (
                  <GridItem 
                    colSpan={"colSpan" in formfield ? formfield.colSpan : gridWidths}
                    key={idx}
                  >
                    <Field 
                      name={formfield.id} 
                      validate={formfield.validator}
                    >
                      {({ field, form }) => (
                        <FormControl
                          isRequired={formfield?.required ? true : false}
                          isInvalid={form.errors[formfield.id] && form.touched[formfield.id]}
                          id={formfield.id} 
                        >
                          <FormLabel {...baseStyle}>
                            {formfield.text}
                          </FormLabel>
                          <Input
                            {...field} 
                            bg='white' 
                            placeholder={formfield.placeholder} 
                          />
                          <FormErrorMessage>
                            {form.errors[formfield.id]}
                          </FormErrorMessage>
                        </FormControl>
                      )}
                    </Field>
                  </GridItem>
                )
              })}
              <GridItem colSpan={{base: 2, lg: 1}}>
                <Button
                  size="lg"
                  borderRadius={["0"]}
                  border={"1px"}
                  bg="mango"
                  w="full"
                  loadingText='Submitting'
                  spinnerPlacement='start'
                  isLoading={props.isSubmitting}
                  type='submit'
                >
                  Join
                </Button>
              </GridItem>
          </SimpleGrid>
        </Form>
      )}
    </Formik>
  )
}

export const SignupForm = (props) => {
  return (
    <Flex
      bg="pololight"
      w="full"
      h="full"
      px={{base: "18px", lg: "35px"}}
      py={{base: "35px", lg: "49px"}}
      border={"1px"}
    >
      <SignupBase location={props.location}/>
    </Flex>
  )
}