import { Span } from "opentracing";
import { DocumentNode, GraphQLSchema, Source, GraphQLError, ExecutionResult } from "graphql";
import { Store } from "redux";
import { IGatsbyState } from "../redux/types";
import { IGraphQLRunnerStatResults, IGraphQLRunnerStats } from "./types";
import { IGraphQLTelemetryRecord } from "../schema/type-definitions";
declare type Query = string | Source;
export interface IQueryOptions {
    parentSpan: Span | undefined;
    queryName: string;
    componentPath?: string | undefined;
    forceGraphqlTracing?: boolean;
    telemetryResolverTimings?: Array<IGraphQLTelemetryRecord>;
}
export interface IGraphQLRunnerOptions {
    collectStats?: boolean;
    graphqlTracing?: boolean;
}
export declare class GraphQLRunner {
    protected store: Store<IGatsbyState>;
    parseCache: Map<Query, DocumentNode>;
    nodeModel: any;
    schema: GraphQLSchema;
    validDocuments: WeakSet<DocumentNode>;
    scheduleClearCache: () => void;
    stats: IGraphQLRunnerStats | null;
    graphqlTracing: boolean;
    constructor(store: Store<IGatsbyState>, { collectStats, graphqlTracing }?: IGraphQLRunnerOptions);
    clearCache(): void;
    parse(query: Query): DocumentNode;
    validate(schema: GraphQLSchema, document: DocumentNode): {
        errors: ReadonlyArray<GraphQLError>;
        warnings: ReadonlyArray<GraphQLError>;
    };
    getStats(): IGraphQLRunnerStatResults | null;
    query(query: Query, context: Record<string, unknown>, { parentSpan, queryName, componentPath, forceGraphqlTracing, telemetryResolverTimings, }: IQueryOptions): Promise<ExecutionResult>;
}
export {};
