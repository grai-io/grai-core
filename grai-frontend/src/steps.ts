import { ShepherdOptionsWithType } from "react-shepherd"
import { offset, shift } from "@floating-ui/dom"

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
    text: [
      "React-Shepherd is a JavaScript library for guiding users through your React app.",
    ],
  },
  {
    id: "add-connection",
    attachTo: {
      element: ".add-connection",
      on: "left" as const,
    },
    classes: "custom-class-name-1 custom-class-name-2",
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Add your first connection",
    text: [
      "Connections are used to import metadata from the data tools in your stack.",
    ],
    advanceOn: { selector: ".add-connection a", event: "click" },
    floatingUIOptions: { middleware: [offset(10)] },
  },
  {
    id: "choose-connection",
    attachTo: {
      element: "body",
      on: "top-end" as const,
    },
    arrow: false,
    floatingUIOptions: {
      middleware: [
        offset(10),
        shift({
          padding: 10,
        }),
      ],
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Choose an integration type",
    text: ["Grai has integrations for a wide variety of data tools."],
    advanceOn: { selector: ".connector-card", event: "click" },
  },
  {
    id: "detail-connection",
    attachTo: {
      element: ".create-connection-wizard",
      on: "top-end" as const,
    },
    arrow: false,
    floatingUIOptions: {
      middleware: [
        offset(10),
        shift({
          padding: 10,
        }),
      ],
    },
    highlightClass: "highlight",
    cancelIcon: {
      enabled: true,
    },
    title: "Enter connection details",
    text: ["You will need to enter some details about your connection."],
    buttons: [
      {
        classes: "shepherd-button-primary",
        text: "Next",
        type: "next",
      },
    ],
  },
  {
    id: "choose-connection",
    attachTo: {
      element: "button[type=submit]",
      on: "top-end" as const,
    },
    arrow: false,
    floatingUIOptions: {
      middleware: [
        offset(10),
        shift({
          padding: 10,
        }),
      ],
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Enter connection details",
    text: ["Press Continue to test your connection."],
    buttons: [
      {
        classes: "shepherd-button-secondary",
        text: "Back",
        type: "back",
      },
    ],
    advanceOn: { selector: "button[type=submit]", event: "click" },
  },
  {
    id: "continue-connection",
    attachTo: {
      element: "button[type=submit]",
      on: "top-end" as const,
    },
    arrow: false,
    floatingUIOptions: {
      middleware: [
        offset(10),
        shift({
          padding: 10,
        }),
      ],
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Wait for connection tests to pass",
    text: ["Grai will test your connection to make sure it works."],
    buttons: [
      {
        classes: "shepherd-button-secondary",
        text: "Back",
        type: "back",
      },
      {
        classes: "shepherd-button-primary",
        text: "Next",
        type: "next",
      },
    ],
  },
  {
    id: "continue-connection",
    attachTo: {
      element: "button[type=submit]",
      on: "top-end" as const,
    },
    arrow: false,
    floatingUIOptions: {
      middleware: [
        offset(10),
        shift({
          padding: 10,
        }),
      ],
    },
    highlightClass: "highlight",
    scrollTo: false,
    cancelIcon: {
      enabled: true,
    },
    title: "Wait for connection tests to pass",
    text: ["Press Continue."],
    buttons: [
      {
        classes: "shepherd-button-secondary",
        text: "Back",
        type: "back",
      },
    ],
    advanceOn: { selector: "button[type=submit]", event: "click" },
  },
]

export default steps
