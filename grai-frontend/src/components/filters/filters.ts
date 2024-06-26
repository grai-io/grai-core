export type Filter = {
  type: string | null
  field: string | null
  operator: string | null
  value: string | string[] | null
}

export interface OperationOption {
  value: string
  label: string
}

export type Operator = {
  value: string
  label: string
  shortLabel?: string
  options?: (string | OperationOption)[]
  multiple?: boolean
}

export type Field = {
  value: string
  label: string
  disabled?: boolean
  operators: Operator[]
}

export type Property = {
  value: string
  label: string
  disabled?: boolean
  fields: Field[]
}

export interface Source {
  id: string
  name: string
}

export const defaultFilter: Filter = {
  type: "table",
  field: null,
  operator: null,
  value: null,
}

const nameField: Field = {
  value: "name",
  label: "Name",
  operators: [
    {
      value: "equals",
      label: "Equals",
      shortLabel: "=",
    },
    {
      value: "contains",
      label: "Contains",
      shortLabel: "*a*",
    },
    {
      value: "starts-with",
      label: "Starts With",
      shortLabel: "a*",
    },
    {
      value: "ends-with",
      label: "Ends With",
      shortLabel: "*a",
    },
    {
      value: "not-equals",
      label: "Not Equals",
      shortLabel: "!=",
    },
    {
      value: "not-contains",
      label: "Not Contains",
      shortLabel: "!*a*",
    },
  ],
}

const namespaceField = (namespaces: string[]): Field => ({
  value: "namespace",
  label: "Namespace",
  operators: [
    {
      value: "equals",
      label: "Equals",
      options: namespaces,
    },
    {
      value: "in",
      label: "In",
      options: namespaces,
      multiple: true,
    },
  ],
})

const sourceField = (sources: Source[]): Field => ({
  value: "data-source",
  label: "Data Source",
  operators: [
    {
      value: "in",
      label: "In",
      options: sources.map(source => ({
        value: source.id,
        label: source.name,
      })),
      multiple: true,
    },
    {
      value: "not-in",
      label: "Not In",
      options: sources.map(source => ({
        value: source.id,
        label: source.name,
      })),
      multiple: true,
    },
  ],
})

const tagField = (tags: string[]): Field => ({
  value: "tag",
  label: "Tag",
  operators: [
    {
      value: "contains",
      label: "Contains",
      options: tags,
    },
    {
      value: "not-contains",
      label: "Doesn't Contain",
      options: tags,
    },
  ],
})

export const getProperties = (
  namespaces: string[],
  tags: string[],
  sources: Source[],
): Property[] => [
  {
    value: "table",
    label: "Default",
    fields: [
      nameField,
      namespaceField(namespaces),
      sourceField(sources),
      tagField(tags),
    ],
  },
  {
    value: "parent",
    label: "Has Parent",
    disabled: true,
    fields: [],
  },
  {
    value: "no-parent",
    label: "No Parent",
    disabled: true,
    fields: [],
  },
  {
    value: "child",
    label: "Has Child",
    disabled: true,
    fields: [],
  },
  {
    value: "no-child",
    label: "No Child",
    disabled: true,
    fields: [],
  },
  {
    value: "ancestor",
    label: "Has Ancestor",
    fields: [tagField(tags)],
  },
  {
    value: "no-ancestor",
    label: "No Ancestor",
    fields: [tagField(tags)],
  },
  {
    value: "descendant",
    label: "Has Descendant",
    fields: [tagField(tags)],
  },
  {
    value: "no-descendant",
    label: "No Descendant",
    fields: [tagField(tags)],
  },
]
