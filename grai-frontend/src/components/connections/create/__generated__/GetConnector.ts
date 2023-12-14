/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnector
// ====================================================

export interface GetConnector_connector {
  __typename: "Connector";
  id: any;
  priority: number | null;
  name: string;
  metadata: any;
  icon: string | null;
  category: string | null;
  status: string;
}

export interface GetConnector {
  connector: GetConnector_connector;
}

export interface GetConnectorVariables {
  connectorId: string;
}
