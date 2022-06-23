import { GraphQLFieldResolver } from "gatsby/graphql";
import { EnumTypeComposerAsObjectDefinition, ObjectTypeComposerFieldConfigAsObjectDefinition, ObjectTypeComposerArgumentConfigMapDefinition } from "graphql-compose";
import { ISharpGatsbyImageArgs, IImageSizeArgs } from "./image-utils";
export declare const ImageFormatType: EnumTypeComposerAsObjectDefinition;
export declare const ImageLayoutType: EnumTypeComposerAsObjectDefinition;
export declare const ImagePlaceholderType: EnumTypeComposerAsObjectDefinition;
export interface IGatsbyGraphQLFieldConfig<TSource, TContext, TArgs> {
    description?: string;
    type: string;
    args?: Record<string, IGatsbyGraphQLResolverArgumentConfig>;
    resolve: GraphQLFieldResolver<TSource, TContext, TArgs>;
}
export interface IGatsbyGraphQLResolverArgumentConfig<TValue = any> {
    description?: string;
    type: string | Array<string>;
    defaultValue?: TValue;
}
export declare type IGatsbyImageResolverArgs = Pick<ISharpGatsbyImageArgs & IImageSizeArgs, "aspectRatio" | "backgroundColor" | "breakpoints" | "height" | "layout" | "outputPixelDensities" | "sizes" | "width">;
export declare function getGatsbyImageResolver<TSource, TContext, TArgs>(resolve: GraphQLFieldResolver<TSource, TContext, IGatsbyImageResolverArgs & TArgs>, extraArgs?: ObjectTypeComposerArgumentConfigMapDefinition<TArgs>): ObjectTypeComposerFieldConfigAsObjectDefinition<TSource, TContext, IGatsbyImageResolverArgs & TArgs>;
export declare type IGatsbyImageFieldArgs = Pick<ISharpGatsbyImageArgs & IImageSizeArgs, "aspectRatio" | "backgroundColor" | "breakpoints" | "formats" | "height" | "layout" | "outputPixelDensities" | "placeholder" | "sizes" | "width">;
export declare function getGatsbyImageFieldConfig<TSource, TContext, TArgs>(resolve: GraphQLFieldResolver<TSource, TContext, IGatsbyImageFieldArgs & TArgs>, extraArgs?: ObjectTypeComposerArgumentConfigMapDefinition<TArgs>): ObjectTypeComposerFieldConfigAsObjectDefinition<TSource, TContext, IGatsbyImageFieldArgs & TArgs>;
