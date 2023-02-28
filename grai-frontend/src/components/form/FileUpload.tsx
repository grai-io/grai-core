import React, { useCallback, useState } from "react"
import { Close } from "@mui/icons-material"
import { Box, Alert } from "@mui/material"
import { Accept, FileRejection, useDropzone } from "react-dropzone"

type FileUploadProps = {
  accept?: Accept | undefined
  value: File | null
  onChange: (file: File | null) => void
}

const FileUpload: React.FC<FileUploadProps> = ({ accept, value, onChange }) => {
  const [rejections, setRejections] = useState<FileRejection[] | null>(null)

  const onDropAccepted = useCallback(
    (files: File[]) => {
      setRejections(null)
      onChange(files[0])
    },
    [onChange]
  )

  const onDropRejected = useCallback((fileRejections: FileRejection[]) => {
    setRejections(fileRejections)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDropAccepted,
    onDropRejected,
    accept,
  })

  const clearFile = () => onChange(null)

  return (
    <>
      {value ? (
        <Box sx={{ display: "flex" }}>
          <Box sx={{ flexGrow: 1 }}>{value.name}</Box>
          <Box>
            <Close onClick={clearFile} sx={{ cursor: "pointer" }} />
          </Box>
        </Box>
      ) : (
        <Box
          sx={{
            borderWidth: 2,
            borderColor: "divider",
            borderStyle: "dashed",
            textAlign: "center",
            py: 10,
            cursor: "pointer",
            backgroundColor: isDragActive
              ? theme => theme.palette.grey[100]
              : undefined,
          }}
          {...getRootProps()}
          data-testid="drop-input"
        >
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop the files here</p>
          ) : (
            <p>Drag and drop some files here, or click to select files</p>
          )}
        </Box>
      )}
      {rejections && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {rejections.map((rejection, index) => (
            <Box key={index}>{rejection.errors[0].message}</Box>
          ))}
        </Alert>
      )}
    </>
  )
}

export default FileUpload
