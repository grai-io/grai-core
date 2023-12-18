/* istanbul ignore file */
import React from "react"
import BaseMarkdown from "react-markdown"
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter"
import { dark, prism, materialDark } from "react-syntax-highlighter/dist/cjs/styles/prism"
import remarkGfm from "remark-gfm"

type MarkdownProps = {
  message: string | null | undefined
}

const Markdown: React.FC<MarkdownProps> = ({ message }) => {
  const remarkPlugins = [remarkGfm]
  const inlineCodeStyle = {
    backgroundColor: '#f5f5f5',
    color: '#8338ec',
    padding: '0.2em 0.4em',
    borderRadius: '6px',
    fontSize: '0.85em'
  };

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
              style={materialDark}
            />
          ) : (
            <code {...rest} className={className} style={inlineCodeStyle}>
              {children}
            </code>
          )
        },
        table: ({ children }) => <table style={{ width: "100%", borderCollapse: "collapse" }}>{children}</table>,
        thead: ({ children }) => <thead>{children}</thead>,
        tbody: ({ children }) => <tbody>{children}</tbody>,
        tr: ({ children }) => <tr>{children}</tr>,
        td: ({ children }) => <td style={{ border: "1px solid black", padding: "5px" }}>{children}</td>,
        th: ({ children }) => <th style={{ border: "1px solid black", padding: "5px" }}>{children}</th>,
      }}
    >
      {message}
    </BaseMarkdown>
  )
}

export default Markdown
