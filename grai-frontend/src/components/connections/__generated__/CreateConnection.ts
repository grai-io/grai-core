/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { OperationMessageKind } from "./../../../../__generated__/globalTypes";

// ====================================================
// GraphQL mutation operation: CreateConnection
// ====================================================

export interface CreateConnection_createConnection_OperationInfo_messages {
  __typename: "OperationMessage";
  /**
   * The kind of this message.
   */
  kind: OperationMessageKind;
  /**
   * The error message.
   */
  message: string;
  /**
   * The field that caused the error, or `null` if it isn't associated with any particular field.
   */
  field: string | null;
}

export interface CreateConnection_createConnection_OperationInfo {
  __typename: "OperationInfo";
  /**
   * List of messages returned by the operation.
   */
  messages: CreateConnection_createConnection_OperationInfo_messages[];
}

export interface CreateConnection_createConnection_ConnectionType_connector {
  __typename: "ConnectorType";
  id: any;
  name: string;
}

export interface CreateConnection_createConnection_ConnectionType {
  __typename: "ConnectionType";
  id: any;
  connector: CreateConnection_createConnection_ConnectionType_connector;
  namespace: string;
  name: string;
  metadata: any;
  isActive: boolean;
  createdAt: any;
  updatedAt: any;
}

export type CreateConnection_createConnection = CreateConnection_createConnection_OperationInfo | CreateConnection_createConnection_ConnectionType;

export interface CreateConnection {
  createConnection: CreateConnection_createConnection;
}

export interface CreateConnectionVariables {
  connector: string;
  namespace?: string | null;
  name: string;
  metadata: any;
  secrets: any;
}
