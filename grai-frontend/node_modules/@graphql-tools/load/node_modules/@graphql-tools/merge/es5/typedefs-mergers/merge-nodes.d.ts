import { Config } from './merge-typedefs';
import { DefinitionNode, NameNode, SchemaDefinitionNode, SchemaExtensionNode } from 'graphql';
export declare const schemaDefSymbol = "SCHEMA_DEF_SYMBOL";
export declare type MergedResultMap = Record<string, NamedDefinitionNode> & {
    [schemaDefSymbol]: SchemaDefinitionNode | SchemaExtensionNode;
};
export declare type NamedDefinitionNode = DefinitionNode & {
    name?: NameNode;
};
export declare function isNamedDefinitionNode(definitionNode: DefinitionNode): definitionNode is NamedDefinitionNode;
export declare function mergeGraphQLNodes(nodes: ReadonlyArray<DefinitionNode>, config?: Config): MergedResultMap;
