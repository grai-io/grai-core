import "../../utils/engines-fs-provider";
import { ExecutionResult, Source } from "graphql";
import { IQueryOptions } from "../../query/graphql-runner";
import type { IGatsbyPage } from "../../redux/types";
export declare class GraphQLEngine {
    private runnerPromise?;
    constructor({ dbPath }: {
        dbPath: string;
    });
    private _doGetRunner;
    private getRunner;
    ready(): Promise<void>;
    runQuery(query: string | Source, context?: Record<string, any>, opts?: IQueryOptions): Promise<ExecutionResult>;
    findPageByPath(pathName: string): IGatsbyPage | undefined;
}
declare const _default: {
    GraphQLEngine: typeof GraphQLEngine;
};
export default _default;
