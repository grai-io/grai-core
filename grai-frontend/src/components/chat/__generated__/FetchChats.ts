/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: FetchChats
// ====================================================

export interface FetchChats_fetchOrCreateChats_data_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface FetchChats_fetchOrCreateChats_data_messages {
  __typename: "MessagePagination";
  data: FetchChats_fetchOrCreateChats_data_messages_data[];
}

export interface FetchChats_fetchOrCreateChats_data {
  __typename: "Chat";
  id: any;
  messages: FetchChats_fetchOrCreateChats_data_messages;
}

export interface FetchChats_fetchOrCreateChats {
  __typename: "ChatDataWrapper";
  data: FetchChats_fetchOrCreateChats_data[];
}

export interface FetchChats {
  fetchOrCreateChats: FetchChats_fetchOrCreateChats;
}

export interface FetchChatsVariables {
  workspaceId: string;
}
