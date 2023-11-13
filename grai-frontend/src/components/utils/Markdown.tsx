/* istanbul ignore file */
import React from "react"
import BaseMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { dark } from "react-syntax-highlighter/dist/cjs/styles/prism"
import remarkGfm from "remark-gfm"

type MarkdownProps = {
  message: string | null | undefined
}

const Markdown: React.FC<MarkdownProps> = ({ message }) => {
  const remarkPlugins = [remarkGfm]

  return (
    <BaseMarkdown
      remarkPlugins={remarkPlugins}
      components={{
        p: ({ children }) => <>{children}</>,
        code: ({ children, className, node, ref, ...rest }) => {
          const match = /language-(\w+)/.exec(className || "")

          return match ? (
            <SyntaxHighlighter
              {...rest}
              PreTag="div"
              children={String(children).replace(/\n$/, "")}
              language={match[1]}
              style={dark}
            />
          ) : (
            <code {...rest} className={className}>
              {children}
            </code>
          )
        },
      }}
    >
      {message}
    </BaseMarkdown>
  )
}

export default Markdown
