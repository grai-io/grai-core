import { watch } from "../utils/webpack/bundle";
import { IWebpackWatchingPauseResume } from "../utils/start-server";
import webpack from "webpack";
import { Span } from "opentracing";
import { IProgram, Stage } from "./types";
import { PackageJson } from "../..";
import type { GatsbyWorkerPool } from "../utils/worker/pool";
declare type IActivity = any;
export interface IBuildArgs extends IProgram {
    directory: string;
    sitePackageJson: PackageJson;
    prefixPaths: boolean;
    noUglify: boolean;
    logPages: boolean;
    writeToFile: boolean;
    profile: boolean;
    graphqlTracing: boolean;
    openTracingConfigFile: string;
    keepPageRenderer: boolean;
}
interface IBuildRendererResult {
    rendererPath: string;
    stats: webpack.Stats;
    close: ReturnType<typeof watch>["close"];
}
declare let devssrWebpackCompiler: webpack.Watching | undefined;
declare let needToRecompileSSRBundle: boolean;
export declare const getDevSSRWebpack: () => {
    devssrWebpackWatcher: IWebpackWatchingPauseResume;
    devssrWebpackCompiler: webpack.Compiler;
    needToRecompileSSRBundle: boolean;
};
export declare const buildRenderer: (program: IProgram, stage: Stage, parentSpan?: IActivity) => Promise<IBuildRendererResult>;
export declare const deleteRenderer: (rendererPath: string) => Promise<void>;
export interface IRenderHtmlResult {
    unsafeBuiltinsUsageByPagePath: Record<string, Array<string>>;
    previewErrors: Record<string, any>;
}
export declare const doBuildPages: (rendererPath: string, pagePaths: Array<string>, activity: IActivity, workerPool: GatsbyWorkerPool, stage: Stage) => Promise<void>;
export declare const buildHTML: ({ program, stage, pagePaths, activity, workerPool, }: {
    program: IProgram;
    stage: Stage;
    pagePaths: Array<string>;
    activity: IActivity;
    workerPool: GatsbyWorkerPool;
}) => Promise<void>;
export declare function buildHTMLPagesAndDeleteStaleArtifacts({ workerPool, parentSpan, program, }: {
    workerPool: GatsbyWorkerPool;
    parentSpan?: Span;
    program: IBuildArgs;
}): Promise<{
    toRegenerate: Array<string>;
    toDelete: Array<string>;
}>;
export {};
