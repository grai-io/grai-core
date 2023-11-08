/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL fragment: NewChat
// ====================================================

export interface NewChat_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface NewChat_messages {
  __typename: "MessagePagination";
  data: NewChat_messages_data[];
}

export interface NewChat {
  __typename: "Chat";
  id: any;
  messages: NewChat_messages;
}
