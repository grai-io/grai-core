import { GraphQLSchema, BuildSchemaOptions } from 'graphql';
import { Config } from './typedefs-mergers/merge-typedefs';
import { IResolvers, IResolverValidationOptions, TypeSource } from '@graphql-tools/utils';
/**
 * Configuration object for schema merging
 */
export interface MergeSchemasConfig<Resolvers extends IResolvers = IResolvers> extends Config, BuildSchemaOptions {
    /**
     * The schemas to be merged
     */
    schemas: GraphQLSchema[];
    /**
     * Additional type definitions to also merge
     */
    typeDefs?: TypeSource;
    /**
     * Additional resolvers to also merge
     */
    resolvers?: Resolvers | Resolvers[];
    /**
     * Options to validate the resolvers being merged, if provided
     */
    resolverValidationOptions?: IResolverValidationOptions;
}
/**
 * Synchronously merges multiple schemas, typeDefinitions and/or resolvers into a single schema.
 * @param config Configuration object
 */
export declare function mergeSchemas(config: MergeSchemasConfig): GraphQLSchema;
/**
 * Asynchronously merges multiple schemas, typeDefinitions and/or resolvers into a single schema.
 * @param config Configuration object
 */
export declare function mergeSchemasAsync(config: MergeSchemasConfig): Promise<GraphQLSchema>;
