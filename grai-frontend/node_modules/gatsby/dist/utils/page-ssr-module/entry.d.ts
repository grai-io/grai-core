import "../engines-fs-provider";
import type { GraphQLEngine } from "../../schema/graphql-engine/entry";
import type { IExecutionResult } from "../../query/types";
import type { IGatsbyPage } from "../../redux/types";
import { IGraphQLTelemetryRecord } from "../../schema/type-definitions";
import type { IScriptsAndStyles } from "../client-assets-for-template";
import type { IPageDataWithQueryResult } from "../page-data";
import type { Request } from "express";
import type { Span, SpanContext } from "opentracing";
export interface ITemplateDetails {
    query: string;
    staticQueryHashes: Array<string>;
    assets: IScriptsAndStyles;
}
export interface ISSRData {
    results: IExecutionResult;
    page: IGatsbyPage;
    templateDetails: ITemplateDetails;
    potentialPagePath: string;
    serverDataHeaders?: Record<string, string>;
    serverDataStatus?: number;
    searchString: string;
}
declare global {
    const INLINED_TEMPLATE_TO_DETAILS: Record<string, ITemplateDetails>;
    const WEBPACK_COMPILATION_HASH: string;
}
export declare function getData({ pathName, graphqlEngine, req, spanContext, telemetryResolverTimings, }: {
    graphqlEngine: GraphQLEngine;
    pathName: string;
    req?: Partial<Pick<Request, "query" | "method" | "url" | "headers">>;
    spanContext?: Span | SpanContext;
    telemetryResolverTimings?: Array<IGraphQLTelemetryRecord>;
}): Promise<ISSRData>;
export declare function renderPageData({ data, spanContext, }: {
    data: ISSRData;
    spanContext?: Span | SpanContext;
}): Promise<IPageDataWithQueryResult>;
export declare function renderHTML({ data, pageData, spanContext, }: {
    data: ISSRData;
    pageData?: IPageDataWithQueryResult;
    spanContext?: Span | SpanContext;
}): Promise<string>;
