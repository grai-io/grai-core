import React, { ReactNode } from "react"

interface FormProps {
  children?: ReactNode
  onSubmit?: React.FormEventHandler<HTMLFormElement>
}

const Form: React.FC<FormProps> = ({ children, onSubmit, ...rest }) => {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    event.stopPropagation()

    onSubmit && onSubmit(event)
  }

  return (
    <form onSubmit={handleSubmit} {...rest}>
      {children}
    </form>
  )
}

export default Form
