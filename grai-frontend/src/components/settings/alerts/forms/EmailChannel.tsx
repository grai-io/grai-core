import React from "react"
import MultipleEmails from "components/form/fields/MultipleEmails"

type EmailChannelProps = {
  value: any
  onChange: (value: any) => void
  disabled?: boolean
}

const EmailChannel: React.FC<EmailChannelProps> = ({
  value,
  onChange,
  disabled,
}) => (
  <MultipleEmails
    value={value.emails ?? []}
    onChange={emails => onChange({ emails })}
    margin="normal"
    disabled={disabled}
  />
)

export default EmailChannel
