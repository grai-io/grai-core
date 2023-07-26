import { offset } from "@floating-ui/dom"
import { ShepherdOptionsWithType } from "react-shepherd"

const steps: ShepherdOptionsWithType[] = [
  {
    id: "intro",
    attachTo: { element: ".first-element", on: "bottom" as const },
    beforeShowPromise: () =>
      new Promise(function (resolve) {
        setTimeout(function () {
          window.scrollTo(0, 0)
          resolve(null)
        }, 500)
      }),
    buttons: [
      {
        classes: "shepherd-button-secondary",
        text: "Close",
        type: "cancel",
      },
      {
        classes: "shepherd-button-primary",
        text: "Next",
        type: "next",
      },
    ],
    highlightClass: "highlight",
    cancelIcon: {
      enabled: true,
    },
    title: "Welcome to Grai!",
    text: "Follow along our tour to get started with Grai and see what it can do for you.",
  },
  {
    id: "view-graph",
    attachTo: {
      element: ".graph-page",
      on: "left" as const,
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "View Graph",
    text: [
      "Your data lineage graph shows each of your data sources and how they are connected.",
    ],
    advanceOn: { selector: ".graph-page a", event: "click" },
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "view-graph-drag",
    // attachTo: {
    //   element: ".graph-page",
    //   on: "left" as const,
    // },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Graph",
    text: [
      "You can drag and zoom in and out on the graph to see additional tables and edges",
    ],
    buttons: [
      {
        classes: "shepherd-button-primary",
        text: "Next",
        type: "next",
      },
    ],
  },
  {
    id: "graph-search",
    attachTo: {
      element: ".graph-search",
      on: "left" as const,
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Graph Search",
    text: [
      "Click on the search icon to search for a table or column in your graph.",
    ],
    advanceOn: { selector: ".graph-search", event: "click" },
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "graph-filter",
    attachTo: {
      element: ".graph-filter",
      on: "left" as const,
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Graph Filter",
    text: ["Click on the filter icon to create and apply filters."],
    advanceOn: { selector: ".graph-filter", event: "click" },
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "graph-table-expand",
    attachTo: {
      element: ".table-expand",
      on: "left" as const,
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Table Expand",
    text: [
      "Click on the expand icon to show the columns in a table and their relationships.",
    ],
    advanceOn: { selector: ".table-expand", event: "click" },
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "graph-table-context-menu",
    attachTo: {
      element: ".graph-table",
      on: "left" as const,
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Table Menu",
    text: "Right clicking on a table will show a menu with additional options.<br />Double clicking will take you to the table details page.",
    buttons: [
      {
        classes: "shepherd-button-primary",
        text: "Next",
        type: "next",
      },
    ],
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "end",
    buttons: [
      {
        classes: "shepherd-button-primary",
        text: "Finish",
        type: "cancel",
      },
    ],
    highlightClass: "highlight",
    cancelIcon: {
      enabled: true,
    },
    title: "Tour complete",
    text: "You can now explore the other pages from the menu on the left.<br />To change settings or log out, click on Profile.<br />To create a new workspace, click on Profile and then Workspaces.<br />To get started you will want to create your first connection.",
  },
]

// const stepsOld: ShepherdOptionsWithType[] = [
//   {
//     id: "intro",
//     attachTo: { element: ".first-element", on: "bottom" as const },
//     beforeShowPromise: () =>
//       new Promise(function (resolve) {
//         setTimeout(function () {
//           window.scrollTo(0, 0)
//           resolve(null)
//         }, 500)
//       }),
//     buttons: [
//       {
//         classes: "shepherd-button-secondary",
//         text: "Close",
//         type: "cancel",
//       },
//       {
//         classes: "shepherd-button-primary",
//         text: "Next",
//         type: "next",
//       },
//     ],
//     highlightClass: "highlight",
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Welcome to Grai!",
//     text: [
//       "React-Shepherd is a JavaScript library for guiding users through your React app.",
//     ],
//   },
//   {
//     id: "add-connection",
//     attachTo: {
//       element: ".add-connection",
//       on: "left" as const,
//     },
//     classes: "custom-class-name-1 custom-class-name-2",
//     highlightClass: "highlight",
//     scrollTo: false,
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Add your first connection",
//     text: [
//       "Connections are used to import metadata from the data tools in your stack.",
//     ],
//     advanceOn: { selector: ".add-connection a", event: "click" },
//     floatingUIOptions: { middleware: [offset(10)] },
//   },
//   {
//     id: "choose-connection",
//     attachTo: {
//       element: "body",
//       on: "top-end" as const,
//     },
//     arrow: false,
//     floatingUIOptions: {
//       middleware: [
//         offset(10),
//         shift({
//           padding: 10,
//         }),
//       ],
//     },
//     highlightClass: "highlight",
//     scrollTo: false,
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Choose an integration type",
//     text: ["Grai has integrations for a wide variety of data tools."],
//     advanceOn: { selector: ".connector-card", event: "click" },
//   },
//   {
//     id: "detail-connection",
//     attachTo: {
//       element: ".create-connection-wizard",
//       on: "top-end" as const,
//     },
//     arrow: false,
//     floatingUIOptions: {
//       middleware: [
//         offset(10),
//         shift({
//           padding: 10,
//         }),
//       ],
//     },
//     highlightClass: "highlight",
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Enter connection details",
//     text: ["You will need to enter some details about your connection."],
//     buttons: [
//       {
//         classes: "shepherd-button-primary",
//         text: "Next",
//         type: "next",
//       },
//     ],
//   },
//   {
//     id: "choose-connection",
//     attachTo: {
//       element: "button[type=submit]",
//       on: "top-end" as const,
//     },
//     arrow: false,
//     floatingUIOptions: {
//       middleware: [
//         offset(10),
//         shift({
//           padding: 10,
//         }),
//       ],
//     },
//     highlightClass: "highlight",
//     scrollTo: false,
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Enter connection details",
//     text: ["Press Continue to test your connection."],
//     buttons: [
//       {
//         classes: "shepherd-button-secondary",
//         text: "Back",
//         type: "back",
//       },
//     ],
//     advanceOn: { selector: "button[type=submit]", event: "click" },
//   },
//   {
//     id: "continue-connection",
//     attachTo: {
//       element: "button[type=submit]",
//       on: "top-end" as const,
//     },
//     arrow: false,
//     floatingUIOptions: {
//       middleware: [
//         offset(10),
//         shift({
//           padding: 10,
//         }),
//       ],
//     },
//     highlightClass: "highlight",
//     scrollTo: false,
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Wait for connection tests to pass",
//     text: ["Grai will test your connection to make sure it works."],
//     buttons: [
//       {
//         classes: "shepherd-button-secondary",
//         text: "Back",
//         type: "back",
//       },
//       {
//         classes: "shepherd-button-primary",
//         text: "Next",
//         type: "next",
//       },
//     ],
//   },
//   {
//     id: "continue-connection",
//     attachTo: {
//       element: "button[type=submit]",
//       on: "top-end" as const,
//     },
//     arrow: false,
//     floatingUIOptions: {
//       middleware: [
//         offset(10),
//         shift({
//           padding: 10,
//         }),
//       ],
//     },
//     highlightClass: "highlight",
//     scrollTo: false,
//     cancelIcon: {
//       enabled: true,
//     },
//     title: "Wait for connection tests to pass",
//     text: ["Press Continue."],
//     buttons: [
//       {
//         classes: "shepherd-button-secondary",
//         text: "Back",
//         type: "back",
//       },
//     ],
//     advanceOn: { selector: "button[type=submit]", event: "click" },
//   },
// ]

export default steps
