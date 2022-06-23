import { parse, isNonNullType, GraphQLError, Kind, valueFromAST, print, isObjectType, isListType, isSpecifiedDirective, astFromValue, isSpecifiedScalarType, isIntrospectionType, isInterfaceType, isUnionType, isInputObjectType, isEnumType, isScalarType, GraphQLDeprecatedDirective, specifiedRules, concatAST, validate, buildASTSchema, buildClientSchema, Source, TokenKind, visit, isTypeSystemDefinitionNode, getNamedType, GraphQLString, GraphQLNonNull, GraphQLList, GraphQLID, GraphQLBoolean, GraphQLFloat, GraphQLInt, GraphQLObjectType, GraphQLInterfaceType, GraphQLInputObjectType, GraphQLDirective, GraphQLUnionType, GraphQLEnumType, GraphQLScalarType, isNamedType, getNullableType, isLeafType, GraphQLSchema, isDirective, isCompositeType, doTypesOverlap, getOperationAST, getOperationRootType, TypeNameMetaFieldDef, isAbstractType } from 'graphql';
import { inspect } from 'util';
import { dedentBlockStringValue } from 'graphql/language/blockString.js';
import { collectFields } from 'graphql/execution/execute.js';

const asArray = (fns) => (Array.isArray(fns) ? fns : fns ? [fns] : []);
function isEqual(a, b) {
    if (Array.isArray(a) && Array.isArray(b)) {
        if (a.length !== b.length) {
            return false;
        }
        for (let index = 0; index < a.length; index++) {
            if (a[index] !== b[index]) {
                return false;
            }
        }
        return true;
    }
    return a === b || (!a && !b);
}
function isNotEqual(a, b) {
    return !isEqual(a, b);
}
function isDocumentString(str) {
    // XXX: is-valid-path or is-glob treat SDL as a valid path
    // (`scalar Date` for example)
    // this why checking the extension is fast enough
    // and prevent from parsing the string in order to find out
    // if the string is a SDL
    if (/\.[a-z0-9]+$/i.test(str)) {
        return false;
    }
    try {
        parse(str);
        return true;
    }
    catch (e) { }
    return false;
}
const invalidPathRegex = /[‘“!%&^<=>`]/;
function isValidPath(str) {
    return typeof str === 'string' && !invalidPathRegex.test(str);
}
function compareStrings(a, b) {
    if (String(a) < String(b)) {
        return -1;
    }
    if (String(a) > String(b)) {
        return 1;
    }
    return 0;
}
function nodeToString(a) {
    var _a, _b;
    let name;
    if ('alias' in a) {
        name = (_a = a.alias) === null || _a === void 0 ? void 0 : _a.value;
    }
    if (name == null && 'name' in a) {
        name = (_b = a.name) === null || _b === void 0 ? void 0 : _b.value;
    }
    if (name == null) {
        name = a.kind;
    }
    return name;
}
function compareNodes(a, b, customFn) {
    const aStr = nodeToString(a);
    const bStr = nodeToString(b);
    if (typeof customFn === 'function') {
        return customFn(aStr, bStr);
    }
    return compareStrings(aStr, bStr);
}
function isSome(input) {
    return input != null;
}
function assertSome(input, message = 'Value should be something') {
    if (input == null) {
        throw new Error(message);
    }
}

/**
 * Prepares an object map of argument values given a list of argument
 * definitions and list of argument AST nodes.
 *
 * Note: The returned value is a plain Object with a prototype, since it is
 * exposed to user code. Care should be taken to not pull values from the
 * Object prototype.
 */
function getArgumentValues(def, node, variableValues = {}) {
    var _a;
    const variableMap = Object.entries(variableValues).reduce((prev, [key, value]) => ({
        ...prev,
        [key]: value,
    }), {});
    const coercedValues = {};
    // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
    const argumentNodes = (_a = node.arguments) !== null && _a !== void 0 ? _a : [];
    const argNodeMap = argumentNodes.reduce((prev, arg) => ({
        ...prev,
        [arg.name.value]: arg,
    }), {});
    for (const { name, type: argType, defaultValue } of def.args) {
        const argumentNode = argNodeMap[name];
        if (!argumentNode) {
            if (defaultValue !== undefined) {
                coercedValues[name] = defaultValue;
            }
            else if (isNonNullType(argType)) {
                throw new GraphQLError(`Argument "${name}" of required type "${inspect(argType)}" ` + 'was not provided.', node);
            }
            continue;
        }
        const valueNode = argumentNode.value;
        let isNull = valueNode.kind === Kind.NULL;
        if (valueNode.kind === Kind.VARIABLE) {
            const variableName = valueNode.name.value;
            if (variableValues == null || !variableMap[variableName]) {
                if (defaultValue !== undefined) {
                    coercedValues[name] = defaultValue;
                }
                else if (isNonNullType(argType)) {
                    throw new GraphQLError(`Argument "${name}" of required type "${inspect(argType)}" ` +
                        `was provided the variable "$${variableName}" which was not provided a runtime value.`, valueNode);
                }
                continue;
            }
            isNull = variableValues[variableName] == null;
        }
        if (isNull && isNonNullType(argType)) {
            throw new GraphQLError(`Argument "${name}" of non-null type "${inspect(argType)}" ` + 'must not be null.', valueNode);
        }
        const coercedValue = valueFromAST(valueNode, argType, variableValues);
        if (coercedValue === undefined) {
            // Note: ValuesOfCorrectTypeRule validation should catch this before
            // execution. This is a runtime check to ensure execution does not
            // continue with an invalid argument value.
            throw new GraphQLError(`Argument "${name}" has invalid value ${print(valueNode)}.`, valueNode);
        }
        coercedValues[name] = coercedValue;
    }
    return coercedValues;
}

function getDirectivesInExtensions(node, pathToDirectivesInExtensions = ['directives']) {
    return pathToDirectivesInExtensions.reduce((acc, pathSegment) => (acc == null ? acc : acc[pathSegment]), node === null || node === void 0 ? void 0 : node.extensions);
}
function _getDirectiveInExtensions(directivesInExtensions, directiveName) {
    const directiveInExtensions = directivesInExtensions.filter(directiveAnnotation => directiveAnnotation.name === directiveName);
    if (!directiveInExtensions.length) {
        return undefined;
    }
    return directiveInExtensions.map(directive => { var _a; return (_a = directive.args) !== null && _a !== void 0 ? _a : {}; });
}
function getDirectiveInExtensions(node, directiveName, pathToDirectivesInExtensions = ['directives']) {
    const directivesInExtensions = pathToDirectivesInExtensions.reduce((acc, pathSegment) => (acc == null ? acc : acc[pathSegment]), node === null || node === void 0 ? void 0 : node.extensions);
    if (directivesInExtensions === undefined) {
        return undefined;
    }
    if (Array.isArray(directivesInExtensions)) {
        return _getDirectiveInExtensions(directivesInExtensions, directiveName);
    }
    // Support condensed format by converting to longer format
    // The condensed format does not preserve ordering of directives when  repeatable directives are used.
    // See https://github.com/ardatan/graphql-tools/issues/2534
    const reformattedDirectivesInExtensions = [];
    for (const [name, argsOrArrayOfArgs] of Object.entries(directivesInExtensions)) {
        if (Array.isArray(argsOrArrayOfArgs)) {
            for (const args of argsOrArrayOfArgs) {
                reformattedDirectivesInExtensions.push({ name, args });
            }
        }
        else {
            reformattedDirectivesInExtensions.push({ name, args: argsOrArrayOfArgs });
        }
    }
    return _getDirectiveInExtensions(reformattedDirectivesInExtensions, directiveName);
}
function getDirectives(schema, node, pathToDirectivesInExtensions = ['directives']) {
    const directivesInExtensions = getDirectivesInExtensions(node, pathToDirectivesInExtensions);
    if (directivesInExtensions != null && directivesInExtensions.length > 0) {
        return directivesInExtensions;
    }
    const schemaDirectives = schema && schema.getDirectives ? schema.getDirectives() : [];
    const schemaDirectiveMap = schemaDirectives.reduce((schemaDirectiveMap, schemaDirective) => {
        schemaDirectiveMap[schemaDirective.name] = schemaDirective;
        return schemaDirectiveMap;
    }, {});
    let astNodes = [];
    if (node.astNode) {
        astNodes.push(node.astNode);
    }
    if ('extensionASTNodes' in node && node.extensionASTNodes) {
        astNodes = [...astNodes, ...node.extensionASTNodes];
    }
    const result = [];
    for (const astNode of astNodes) {
        if (astNode.directives) {
            for (const directiveNode of astNode.directives) {
                const schemaDirective = schemaDirectiveMap[directiveNode.name.value];
                if (schemaDirective) {
                    result.push({ name: directiveNode.name.value, args: getArgumentValues(schemaDirective, directiveNode) });
                }
            }
        }
    }
    return result;
}
function getDirective(schema, node, directiveName, pathToDirectivesInExtensions = ['directives']) {
    const directiveInExtensions = getDirectiveInExtensions(node, directiveName, pathToDirectivesInExtensions);
    if (directiveInExtensions != null) {
        return directiveInExtensions;
    }
    const schemaDirective = schema && schema.getDirective ? schema.getDirective(directiveName) : undefined;
    if (schemaDirective == null) {
        return undefined;
    }
    let astNodes = [];
    if (node.astNode) {
        astNodes.push(node.astNode);
    }
    if ('extensionASTNodes' in node && node.extensionASTNodes) {
        astNodes = [...astNodes, ...node.extensionASTNodes];
    }
    const result = [];
    for (const astNode of astNodes) {
        if (astNode.directives) {
            for (const directiveNode of astNode.directives) {
                if (directiveNode.name.value === directiveName) {
                    result.push(getArgumentValues(schemaDirective, directiveNode));
                }
            }
        }
    }
    if (!result.length) {
        return undefined;
    }
    return result;
}

function parseDirectiveValue(value) {
    switch (value.kind) {
        case Kind.INT:
            return parseInt(value.value);
        case Kind.FLOAT:
            return parseFloat(value.value);
        case Kind.BOOLEAN:
            return Boolean(value.value);
        case Kind.STRING:
        case Kind.ENUM:
            return value.value;
        case Kind.LIST:
            return value.values.map(v => parseDirectiveValue(v));
        case Kind.OBJECT:
            return value.fields.reduce((prev, v) => ({ ...prev, [v.name.value]: parseDirectiveValue(v.value) }), {});
        case Kind.NULL:
            return null;
        default:
            return null;
    }
}
function getFieldsWithDirectives(documentNode, options = {}) {
    const result = {};
    let selected = ['ObjectTypeDefinition', 'ObjectTypeExtension'];
    if (options.includeInputTypes) {
        selected = [...selected, 'InputObjectTypeDefinition', 'InputObjectTypeExtension'];
    }
    const allTypes = documentNode.definitions.filter(obj => selected.includes(obj.kind));
    for (const type of allTypes) {
        const typeName = type.name.value;
        if (type.fields == null) {
            continue;
        }
        for (const field of type.fields) {
            if (field.directives && field.directives.length > 0) {
                const fieldName = field.name.value;
                const key = `${typeName}.${fieldName}`;
                const directives = field.directives.map(d => ({
                    name: d.name.value,
                    args: (d.arguments || []).reduce((prev, arg) => ({ ...prev, [arg.name.value]: parseDirectiveValue(arg.value) }), {}),
                }));
                result[key] = directives;
            }
        }
    }
    return result;
}

function getImplementingTypes(interfaceName, schema) {
    const allTypesMap = schema.getTypeMap();
    const result = [];
    for (const graphqlTypeName in allTypesMap) {
        const graphqlType = allTypesMap[graphqlTypeName];
        if (isObjectType(graphqlType)) {
            const allInterfaces = graphqlType.getInterfaces();
            if (allInterfaces.find(int => int.name === interfaceName)) {
                result.push(graphqlType.name);
            }
        }
    }
    return result;
}

function astFromType(type) {
    if (isNonNullType(type)) {
        const innerType = astFromType(type.ofType);
        if (innerType.kind === Kind.NON_NULL_TYPE) {
            throw new Error(`Invalid type node ${JSON.stringify(type)}. Inner type of non-null type cannot be a non-null type.`);
        }
        return {
            kind: Kind.NON_NULL_TYPE,
            type: innerType,
        };
    }
    else if (isListType(type)) {
        return {
            kind: Kind.LIST_TYPE,
            type: astFromType(type.ofType),
        };
    }
    return {
        kind: Kind.NAMED_TYPE,
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
    };
}

/**
 * Produces a GraphQL Value AST given a JavaScript object.
 * Function will match JavaScript/JSON values to GraphQL AST schema format
 * by using the following mapping.
 *
 * | JSON Value    | GraphQL Value        |
 * | ------------- | -------------------- |
 * | Object        | Input Object         |
 * | Array         | List                 |
 * | Boolean       | Boolean              |
 * | String        | String               |
 * | Number        | Int / Float          |
 * | null          | NullValue            |
 *
 */
function astFromValueUntyped(value) {
    // only explicit null, not undefined, NaN
    if (value === null) {
        return { kind: Kind.NULL };
    }
    // undefined
    if (value === undefined) {
        return null;
    }
    // Convert JavaScript array to GraphQL list. If the GraphQLType is a list, but
    // the value is not an array, convert the value using the list's item type.
    if (Array.isArray(value)) {
        const valuesNodes = [];
        for (const item of value) {
            const itemNode = astFromValueUntyped(item);
            if (itemNode != null) {
                valuesNodes.push(itemNode);
            }
        }
        return { kind: Kind.LIST, values: valuesNodes };
    }
    if (typeof value === 'object') {
        const fieldNodes = [];
        for (const fieldName in value) {
            const fieldValue = value[fieldName];
            const ast = astFromValueUntyped(fieldValue);
            if (ast) {
                fieldNodes.push({
                    kind: Kind.OBJECT_FIELD,
                    name: { kind: Kind.NAME, value: fieldName },
                    value: ast,
                });
            }
        }
        return { kind: Kind.OBJECT, fields: fieldNodes };
    }
    // Others serialize based on their corresponding JavaScript scalar types.
    if (typeof value === 'boolean') {
        return { kind: Kind.BOOLEAN, value };
    }
    // JavaScript numbers can be Int or Float values.
    if (typeof value === 'number' && isFinite(value)) {
        const stringNum = String(value);
        return integerStringRegExp.test(stringNum)
            ? { kind: Kind.INT, value: stringNum }
            : { kind: Kind.FLOAT, value: stringNum };
    }
    if (typeof value === 'string') {
        return { kind: Kind.STRING, value };
    }
    throw new TypeError(`Cannot convert value to AST: ${value}.`);
}
/**
 * IntValue:
 *   - NegativeSign? 0
 *   - NegativeSign? NonZeroDigit ( Digit+ )?
 */
const integerStringRegExp = /^-?(?:0|[1-9][0-9]*)$/;

function getDocumentNodeFromSchema(schema, options = {}) {
    const pathToDirectivesInExtensions = options.pathToDirectivesInExtensions;
    const typesMap = schema.getTypeMap();
    const schemaNode = astFromSchema(schema, pathToDirectivesInExtensions);
    const definitions = schemaNode != null ? [schemaNode] : [];
    const directives = schema.getDirectives();
    for (const directive of directives) {
        if (isSpecifiedDirective(directive)) {
            continue;
        }
        definitions.push(astFromDirective(directive, schema, pathToDirectivesInExtensions));
    }
    for (const typeName in typesMap) {
        const type = typesMap[typeName];
        const isPredefinedScalar = isSpecifiedScalarType(type);
        const isIntrospection = isIntrospectionType(type);
        if (isPredefinedScalar || isIntrospection) {
            continue;
        }
        if (isObjectType(type)) {
            definitions.push(astFromObjectType(type, schema, pathToDirectivesInExtensions));
        }
        else if (isInterfaceType(type)) {
            definitions.push(astFromInterfaceType(type, schema, pathToDirectivesInExtensions));
        }
        else if (isUnionType(type)) {
            definitions.push(astFromUnionType(type, schema, pathToDirectivesInExtensions));
        }
        else if (isInputObjectType(type)) {
            definitions.push(astFromInputObjectType(type, schema, pathToDirectivesInExtensions));
        }
        else if (isEnumType(type)) {
            definitions.push(astFromEnumType(type, schema, pathToDirectivesInExtensions));
        }
        else if (isScalarType(type)) {
            definitions.push(astFromScalarType(type, schema, pathToDirectivesInExtensions));
        }
        else {
            throw new Error(`Unknown type ${type}.`);
        }
    }
    return {
        kind: Kind.DOCUMENT,
        definitions,
    };
}
// this approach uses the default schema printer rather than a custom solution, so may be more backwards compatible
// currently does not allow customization of printSchema options having to do with comments.
function printSchemaWithDirectives(schema, options = {}) {
    const documentNode = getDocumentNodeFromSchema(schema, options);
    return print(documentNode);
}
function astFromSchema(schema, pathToDirectivesInExtensions) {
    var _a, _b;
    const operationTypeMap = {
        query: undefined,
        mutation: undefined,
        subscription: undefined,
    };
    const nodes = [];
    if (schema.astNode != null) {
        nodes.push(schema.astNode);
    }
    if (schema.extensionASTNodes != null) {
        for (const extensionASTNode of schema.extensionASTNodes) {
            nodes.push(extensionASTNode);
        }
    }
    for (const node of nodes) {
        if (node.operationTypes) {
            for (const operationTypeDefinitionNode of node.operationTypes) {
                operationTypeMap[operationTypeDefinitionNode.operation] = operationTypeDefinitionNode;
            }
        }
    }
    const rootTypeMap = {
        query: schema.getQueryType(),
        mutation: schema.getMutationType(),
        subscription: schema.getSubscriptionType(),
    };
    for (const operationTypeNode in operationTypeMap) {
        if (rootTypeMap[operationTypeNode] != null) {
            if (operationTypeMap[operationTypeNode] != null) {
                operationTypeMap[operationTypeNode].type = astFromType(rootTypeMap[operationTypeNode]);
            }
            else {
                operationTypeMap[operationTypeNode] = {
                    kind: Kind.OPERATION_TYPE_DEFINITION,
                    operation: operationTypeNode,
                    type: astFromType(rootTypeMap[operationTypeNode]),
                };
            }
        }
    }
    const operationTypes = Object.values(operationTypeMap).filter(isSome);
    const directives = getDirectiveNodes(schema, schema, pathToDirectivesInExtensions);
    if (!operationTypes.length && !directives.length) {
        return null;
    }
    const schemaNode = {
        kind: operationTypes != null ? Kind.SCHEMA_DEFINITION : Kind.SCHEMA_EXTENSION,
        operationTypes,
        directives,
    };
    // This code is so weird because it needs to support GraphQL.js 14
    // In GraphQL.js 14 there is no `description` value on schemaNode
    schemaNode.description =
        ((_b = (_a = schema.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : schema.description != null)
            ? {
                kind: Kind.STRING,
                value: schema.description,
                block: true,
            }
            : undefined;
    return schemaNode;
}
function astFromDirective(directive, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.DIRECTIVE_DEFINITION,
        description: (_b = (_a = directive.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (directive.description
            ? {
                kind: Kind.STRING,
                value: directive.description,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: directive.name,
        },
        arguments: (directive === null || directive === void 0 ? void 0 : directive.args)
            ? directive.args.map(arg => astFromArg(arg, schema, pathToDirectivesInExtensions))
            : undefined,
        repeatable: directive.isRepeatable,
        locations: (directive === null || directive === void 0 ? void 0 : directive.locations)
            ? directive.locations.map(location => ({
                kind: Kind.NAME,
                value: location,
            }))
            : [],
    };
}
function getDirectiveNodes(entity, schema, pathToDirectivesInExtensions) {
    const directivesInExtensions = getDirectivesInExtensions(entity, pathToDirectivesInExtensions);
    let nodes = [];
    if (entity.astNode != null) {
        nodes.push(entity.astNode);
    }
    if ('extensionASTNodes' in entity && entity.extensionASTNodes != null) {
        nodes = nodes.concat(entity.extensionASTNodes);
    }
    let directives;
    if (directivesInExtensions != null) {
        directives = makeDirectiveNodes(schema, directivesInExtensions);
    }
    else {
        directives = [];
        for (const node of nodes) {
            if (node.directives) {
                directives.push(...node.directives);
            }
        }
    }
    return directives;
}
function getDeprecatableDirectiveNodes(entity, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    let directiveNodesBesidesDeprecated = [];
    let deprecatedDirectiveNode = null;
    const directivesInExtensions = getDirectivesInExtensions(entity, pathToDirectivesInExtensions);
    let directives;
    if (directivesInExtensions != null) {
        directives = makeDirectiveNodes(schema, directivesInExtensions);
    }
    else {
        directives = (_a = entity.astNode) === null || _a === void 0 ? void 0 : _a.directives;
    }
    if (directives != null) {
        directiveNodesBesidesDeprecated = directives.filter(directive => directive.name.value !== 'deprecated');
        if (entity.deprecationReason != null) {
            deprecatedDirectiveNode = (_b = directives.filter(directive => directive.name.value === 'deprecated')) === null || _b === void 0 ? void 0 : _b[0];
        }
    }
    if (entity.deprecationReason != null &&
        deprecatedDirectiveNode == null) {
        deprecatedDirectiveNode = makeDeprecatedDirective(entity.deprecationReason);
    }
    return deprecatedDirectiveNode == null
        ? directiveNodesBesidesDeprecated
        : [deprecatedDirectiveNode].concat(directiveNodesBesidesDeprecated);
}
function astFromArg(arg, schema, pathToDirectivesInExtensions) {
    var _a, _b, _c;
    return {
        kind: Kind.INPUT_VALUE_DEFINITION,
        description: (_b = (_a = arg.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (arg.description
            ? {
                kind: Kind.STRING,
                value: arg.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: arg.name,
        },
        type: astFromType(arg.type),
        defaultValue: arg.defaultValue !== undefined ? (_c = astFromValue(arg.defaultValue, arg.type)) !== null && _c !== void 0 ? _c : undefined : undefined,
        directives: getDeprecatableDirectiveNodes(arg, schema, pathToDirectivesInExtensions),
    };
}
function astFromObjectType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.OBJECT_TYPE_DEFINITION,
        description: (_b = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        fields: Object.values(type.getFields()).map(field => astFromField(field, schema, pathToDirectivesInExtensions)),
        interfaces: Object.values(type.getInterfaces()).map(iFace => astFromType(iFace)),
        directives: getDirectiveNodes(type, schema, pathToDirectivesInExtensions),
    };
}
function astFromInterfaceType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    const node = {
        kind: Kind.INTERFACE_TYPE_DEFINITION,
        description: (_b = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        fields: Object.values(type.getFields()).map(field => astFromField(field, schema, pathToDirectivesInExtensions)),
        directives: getDirectiveNodes(type, schema, pathToDirectivesInExtensions),
    };
    if ('getInterfaces' in type) {
        node.interfaces = Object.values(type.getInterfaces()).map(iFace => astFromType(iFace));
    }
    return node;
}
function astFromUnionType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.UNION_TYPE_DEFINITION,
        description: (_b = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        directives: getDirectiveNodes(type, schema, pathToDirectivesInExtensions),
        types: type.getTypes().map(type => astFromType(type)),
    };
}
function astFromInputObjectType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.INPUT_OBJECT_TYPE_DEFINITION,
        description: (_b = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        fields: Object.values(type.getFields()).map(field => astFromInputField(field, schema, pathToDirectivesInExtensions)),
        directives: getDirectiveNodes(type, schema, pathToDirectivesInExtensions),
    };
}
function astFromEnumType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.ENUM_TYPE_DEFINITION,
        description: (_b = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        values: Object.values(type.getValues()).map(value => astFromEnumValue(value, schema, pathToDirectivesInExtensions)),
        directives: getDirectiveNodes(type, schema, pathToDirectivesInExtensions),
    };
}
function astFromScalarType(type, schema, pathToDirectivesInExtensions) {
    var _a, _b, _c, _d;
    let directiveNodesBesidesSpecifiedBy = [];
    let specifiedByDirectiveNode = null;
    const directivesInExtensions = getDirectivesInExtensions(type, pathToDirectivesInExtensions);
    let allDirectives;
    if (directivesInExtensions != null) {
        allDirectives = makeDirectiveNodes(schema, directivesInExtensions);
    }
    else {
        allDirectives = (_a = type.astNode) === null || _a === void 0 ? void 0 : _a.directives;
    }
    if (allDirectives != null) {
        directiveNodesBesidesSpecifiedBy = allDirectives.filter(directive => directive.name.value !== 'specifiedBy');
        if (type.specifiedByUrl != null) {
            specifiedByDirectiveNode = (_b = allDirectives.filter(directive => directive.name.value === 'specifiedBy')) === null || _b === void 0 ? void 0 : _b[0];
        }
    }
    if (type.specifiedByUrl != null && specifiedByDirectiveNode == null) {
        specifiedByDirectiveNode = makeDirectiveNode('specifiedBy', {
            url: type.specifiedByUrl,
        });
    }
    const directives = specifiedByDirectiveNode == null
        ? directiveNodesBesidesSpecifiedBy
        : [specifiedByDirectiveNode].concat(directiveNodesBesidesSpecifiedBy);
    return {
        kind: Kind.SCALAR_TYPE_DEFINITION,
        description: (_d = (_c = type.astNode) === null || _c === void 0 ? void 0 : _c.description) !== null && _d !== void 0 ? _d : (type.description
            ? {
                kind: Kind.STRING,
                value: type.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: type.name,
        },
        directives,
    };
}
function astFromField(field, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.FIELD_DEFINITION,
        description: (_b = (_a = field.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (field.description
            ? {
                kind: Kind.STRING,
                value: field.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: field.name,
        },
        arguments: field.args.map(arg => astFromArg(arg, schema, pathToDirectivesInExtensions)),
        type: astFromType(field.type),
        directives: getDeprecatableDirectiveNodes(field, schema, pathToDirectivesInExtensions),
    };
}
function astFromInputField(field, schema, pathToDirectivesInExtensions) {
    var _a, _b, _c;
    return {
        kind: Kind.INPUT_VALUE_DEFINITION,
        description: (_b = (_a = field.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (field.description
            ? {
                kind: Kind.STRING,
                value: field.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: field.name,
        },
        type: astFromType(field.type),
        directives: getDeprecatableDirectiveNodes(field, schema, pathToDirectivesInExtensions),
        defaultValue: (_c = astFromValue(field.defaultValue, field.type)) !== null && _c !== void 0 ? _c : undefined,
    };
}
function astFromEnumValue(value, schema, pathToDirectivesInExtensions) {
    var _a, _b;
    return {
        kind: Kind.ENUM_VALUE_DEFINITION,
        description: (_b = (_a = value.astNode) === null || _a === void 0 ? void 0 : _a.description) !== null && _b !== void 0 ? _b : (value.description
            ? {
                kind: Kind.STRING,
                value: value.description,
                block: true,
            }
            : undefined),
        name: {
            kind: Kind.NAME,
            value: value.name,
        },
        directives: getDirectiveNodes(value, schema, pathToDirectivesInExtensions),
    };
}
function makeDeprecatedDirective(deprecationReason) {
    return makeDirectiveNode('deprecated', { reason: deprecationReason }, GraphQLDeprecatedDirective);
}
function makeDirectiveNode(name, args, directive) {
    const directiveArguments = [];
    if (directive != null) {
        for (const arg of directive.args) {
            const argName = arg.name;
            const argValue = args[argName];
            if (argValue !== undefined) {
                const value = astFromValue(argValue, arg.type);
                if (value) {
                    directiveArguments.push({
                        kind: Kind.ARGUMENT,
                        name: {
                            kind: Kind.NAME,
                            value: argName,
                        },
                        value,
                    });
                }
            }
        }
    }
    else {
        for (const argName in args) {
            const argValue = args[argName];
            const value = astFromValueUntyped(argValue);
            if (value) {
                directiveArguments.push({
                    kind: Kind.ARGUMENT,
                    name: {
                        kind: Kind.NAME,
                        value: argName,
                    },
                    value,
                });
            }
        }
    }
    return {
        kind: Kind.DIRECTIVE,
        name: {
            kind: Kind.NAME,
            value: name,
        },
        arguments: directiveArguments,
    };
}
function makeDirectiveNodes(schema, directiveValues) {
    const directiveNodes = [];
    for (const directiveName in directiveValues) {
        const arrayOrSingleValue = directiveValues[directiveName];
        const directive = schema === null || schema === void 0 ? void 0 : schema.getDirective(directiveName);
        if (Array.isArray(arrayOrSingleValue)) {
            for (const value of arrayOrSingleValue) {
                directiveNodes.push(makeDirectiveNode(directiveName, value, directive));
            }
        }
        else {
            directiveNodes.push(makeDirectiveNode(directiveName, arrayOrSingleValue, directive));
        }
    }
    return directiveNodes;
}

let AggregateErrorImpl = globalThis.AggregateError;
if (typeof AggregateErrorImpl === 'undefined') {
    class AggregateErrorClass extends Error {
        constructor(errors, message = '') {
            super(message);
            this.errors = errors;
            this.name = 'AggregateError';
            Error.captureStackTrace(this, AggregateErrorClass);
        }
    }
    AggregateErrorImpl = function (errors, message) {
        return new AggregateErrorClass(errors, message);
    };
}

async function validateGraphQlDocuments(schema, documentFiles, effectiveRules) {
    effectiveRules = effectiveRules || createDefaultRules();
    const allFragmentMap = new Map();
    const documentFileObjectsToValidate = [];
    for (const documentFile of documentFiles) {
        if (documentFile.document) {
            const definitionsToValidate = [];
            for (const definitionNode of documentFile.document.definitions) {
                if (definitionNode.kind === Kind.FRAGMENT_DEFINITION) {
                    allFragmentMap.set(definitionNode.name.value, definitionNode);
                }
                else {
                    definitionsToValidate.push(definitionNode);
                }
            }
            documentFileObjectsToValidate.push({
                location: documentFile.location,
                document: {
                    kind: Kind.DOCUMENT,
                    definitions: definitionsToValidate,
                },
            });
        }
    }
    const allErrors = [];
    const allFragmentsDocument = {
        kind: Kind.DOCUMENT,
        definitions: [...allFragmentMap.values()],
    };
    await Promise.all(documentFileObjectsToValidate.map(async (documentFile) => {
        const documentToValidate = concatAST([allFragmentsDocument, documentFile.document]);
        const errors = validate(schema, documentToValidate, effectiveRules);
        if (errors.length > 0) {
            allErrors.push({
                filePath: documentFile.location,
                errors,
            });
        }
    }));
    return allErrors;
}
function checkValidationErrors(loadDocumentErrors) {
    if (loadDocumentErrors.length > 0) {
        const errors = [];
        for (const loadDocumentError of loadDocumentErrors) {
            for (const graphQLError of loadDocumentError.errors) {
                const error = new Error();
                error.name = 'GraphQLDocumentError';
                error.message = `${error.name}: ${graphQLError.message}`;
                error.stack = error.message;
                if (graphQLError.locations) {
                    for (const location of graphQLError.locations) {
                        error.stack += `\n    at ${loadDocumentError.filePath}:${location.line}:${location.column}`;
                    }
                }
                errors.push(error);
            }
        }
        throw new AggregateErrorImpl(errors, `GraphQL Document Validation failed with ${loadDocumentErrors.length} errors`);
    }
}
function createDefaultRules() {
    const ignored = ['NoUnusedFragmentsRule', 'NoUnusedVariablesRule', 'KnownDirectivesRule'];
    const v4ignored = ignored.map(rule => rule.replace(/Rule$/, ''));
    return specifiedRules.filter((f) => !ignored.includes(f.name) && !v4ignored.includes(f.name));
}

function buildFixedSchema(schema, options) {
    const document = getDocumentNodeFromSchema(schema);
    return buildASTSchema(document, {
        ...(options || {}),
    });
}
function fixSchemaAst(schema, options) {
    // eslint-disable-next-line no-undef-init
    let schemaWithValidAst = undefined;
    if (!schema.astNode || !schema.extensionASTNodes) {
        schemaWithValidAst = buildFixedSchema(schema, options);
    }
    if (!schema.astNode && (schemaWithValidAst === null || schemaWithValidAst === void 0 ? void 0 : schemaWithValidAst.astNode)) {
        schema.astNode = schemaWithValidAst.astNode;
    }
    if (!schema.extensionASTNodes && (schemaWithValidAst === null || schemaWithValidAst === void 0 ? void 0 : schemaWithValidAst.astNode)) {
        schema.extensionASTNodes = schemaWithValidAst.extensionASTNodes;
    }
    return schema;
}

function stripBOM(content) {
    content = content.toString();
    // Remove byte order marker. This catches EF BB BF (the UTF-8 BOM)
    // because the buffer-to-string conversion in `fs.readFileSync()`
    // translates it to FEFF, the UTF-16 BOM.
    if (content.charCodeAt(0) === 0xfeff) {
        content = content.slice(1);
    }
    return content;
}
function parseBOM(content) {
    return JSON.parse(stripBOM(content));
}
function parseGraphQLJSON(location, jsonContent, options) {
    let parsedJson = parseBOM(jsonContent);
    if (parsedJson.data) {
        parsedJson = parsedJson.data;
    }
    if (parsedJson.kind === 'Document') {
        return {
            location,
            document: parsedJson,
        };
    }
    else if (parsedJson.__schema) {
        const schema = buildClientSchema(parsedJson, options);
        return {
            location,
            schema,
        };
    }
    else if (typeof parsedJson === 'string') {
        return {
            location,
            rawSDL: parsedJson,
        };
    }
    throw new Error(`Not valid JSON content`);
}

function parseGraphQLSDL(location, rawSDL, options = {}) {
    let document;
    try {
        if (options.commentDescriptions && rawSDL.includes('#')) {
            document = transformCommentsToDescriptions(rawSDL, options);
            // If noLocation=true, we need to make sure to print and parse it again, to remove locations,
            // since `transformCommentsToDescriptions` must have locations set in order to transform the comments
            // into descriptions.
            if (options.noLocation) {
                document = parse(print(document), options);
            }
        }
        else {
            document = parse(new Source(rawSDL, location), options);
        }
    }
    catch (e) {
        if (e.message.includes('EOF') && rawSDL.replace(/(\#[^*]*)/g, '').trim() === '') {
            document = {
                kind: Kind.DOCUMENT,
                definitions: [],
            };
        }
        else {
            throw e;
        }
    }
    return {
        location,
        document,
    };
}
function getLeadingCommentBlock(node) {
    const loc = node.loc;
    if (!loc) {
        return;
    }
    const comments = [];
    let token = loc.startToken.prev;
    while (token != null &&
        token.kind === TokenKind.COMMENT &&
        token.next &&
        token.prev &&
        token.line + 1 === token.next.line &&
        token.line !== token.prev.line) {
        const value = String(token.value);
        comments.push(value);
        token = token.prev;
    }
    return comments.length > 0 ? comments.reverse().join('\n') : undefined;
}
function transformCommentsToDescriptions(sourceSdl, options = {}) {
    const parsedDoc = parse(sourceSdl, {
        ...options,
        noLocation: false,
    });
    const modifiedDoc = visit(parsedDoc, {
        leave: (node) => {
            if (isDescribable(node)) {
                const rawValue = getLeadingCommentBlock(node);
                if (rawValue !== undefined) {
                    const commentsBlock = dedentBlockStringValue('\n' + rawValue);
                    const isBlock = commentsBlock.includes('\n');
                    if (!node.description) {
                        return {
                            ...node,
                            description: {
                                kind: Kind.STRING,
                                value: commentsBlock,
                                block: isBlock,
                            },
                        };
                    }
                    else {
                        return {
                            ...node,
                            description: {
                                ...node.description,
                                value: node.description.value + '\n' + commentsBlock,
                                block: true,
                            },
                        };
                    }
                }
            }
        },
    });
    return modifiedDoc;
}
function isDescribable(node) {
    return (isTypeSystemDefinitionNode(node) ||
        node.kind === Kind.FIELD_DEFINITION ||
        node.kind === Kind.INPUT_VALUE_DEFINITION ||
        node.kind === Kind.ENUM_VALUE_DEFINITION);
}

/**
 * Get all GraphQL types from schema without:
 *
 * - Query, Mutation, Subscription objects
 * - Internal scalars added by parser
 *
 * @param schema
 */
function getUserTypesFromSchema(schema) {
    const allTypesMap = schema.getTypeMap();
    // tslint:disable-next-line: no-unnecessary-local-variable
    const modelTypes = Object.values(allTypesMap).filter((graphqlType) => {
        if (isObjectType(graphqlType)) {
            // Filter out private types
            if (graphqlType.name.startsWith('__')) {
                return false;
            }
            const schemaMutationType = schema.getMutationType();
            if (schemaMutationType && graphqlType.name === schemaMutationType.name) {
                return false;
            }
            const schemaQueryType = schema.getMutationType();
            if (schemaQueryType && graphqlType.name === schemaQueryType.name) {
                return false;
            }
            const schemaSubscriptionType = schema.getMutationType();
            if (schemaSubscriptionType && graphqlType.name === schemaSubscriptionType.name) {
                return false;
            }
            return true;
        }
        return false;
    });
    return modelTypes;
}

function createSchemaDefinition(def, config) {
    const schemaRoot = {};
    if (def.query) {
        schemaRoot.query = def.query.toString();
    }
    if (def.mutation) {
        schemaRoot.mutation = def.mutation.toString();
    }
    if (def.subscription) {
        schemaRoot.subscription = def.subscription.toString();
    }
    const fields = Object.keys(schemaRoot)
        .map(rootType => (schemaRoot[rootType] ? `${rootType}: ${schemaRoot[rootType]}` : null))
        .filter(a => a);
    if (fields.length) {
        return `schema { ${fields.join('\n')} }`;
    }
    if (config && config.force) {
        return ` schema { query: Query } `;
    }
    return undefined;
}

function getDefinedRootType(schema, operation) {
    let rootType;
    if (operation === 'query') {
        rootType = schema.getQueryType();
    }
    else if (operation === 'mutation') {
        rootType = schema.getMutationType();
    }
    else if (operation === 'subscription') {
        rootType = schema.getSubscriptionType();
    }
    else {
        // Future proof against new operation types
        throw new Error(`Unknown operation "${operation}", cannot get root type.`);
    }
    if (rootType == null) {
        throw new Error(`Root type for operation "${operation}" not defined by the given schema.`);
    }
    return rootType;
}
function getRootTypeNames(schema) {
    const rootTypeNames = new Set();
    const queryType = schema.getQueryType();
    const mutationType = schema.getMutationType();
    const subscriptionType = schema.getSubscriptionType();
    for (const rootType of [queryType, mutationType, subscriptionType]) {
        if (rootType) {
            rootTypeNames.add(rootType.name);
        }
    }
    return rootTypeNames;
}
function getRootTypes(schema) {
    const rootTypes = new Set();
    const queryType = schema.getQueryType();
    const mutationType = schema.getMutationType();
    const subscriptionType = schema.getSubscriptionType();
    for (const rootType of [queryType, mutationType, subscriptionType]) {
        if (rootType) {
            rootTypes.add(rootType);
        }
    }
    return rootTypes;
}
function getRootTypeMap(schema) {
    const rootTypeMap = new Map();
    const queryType = schema.getQueryType();
    if (queryType) {
        rootTypeMap.set('query', queryType);
    }
    const mutationType = schema.getMutationType();
    if (mutationType) {
        rootTypeMap.set('mutation', mutationType);
    }
    const subscriptionType = schema.getSubscriptionType();
    if (subscriptionType) {
        rootTypeMap.set('subscription', subscriptionType);
    }
    return rootTypeMap;
}

let operationVariables = [];
let fieldTypeMap = new Map();
function addOperationVariable(variable) {
    operationVariables.push(variable);
}
function resetOperationVariables() {
    operationVariables = [];
}
function resetFieldMap() {
    fieldTypeMap = new Map();
}
function buildOperationNodeForField({ schema, kind, field, models, ignore, depthLimit, circularReferenceDepth, argNames, selectedFields = true, }) {
    resetOperationVariables();
    resetFieldMap();
    const operationNode = buildOperationAndCollectVariables({
        schema,
        fieldName: field,
        kind,
        models: models || [],
        ignore: ignore || [],
        depthLimit: depthLimit || Infinity,
        circularReferenceDepth: circularReferenceDepth || 1,
        argNames,
        selectedFields,
    });
    // attach variables
    operationNode.variableDefinitions = [...operationVariables];
    resetOperationVariables();
    resetFieldMap();
    return operationNode;
}
function buildOperationAndCollectVariables({ schema, fieldName, kind, models, ignore, depthLimit, circularReferenceDepth, argNames, selectedFields, }) {
    const type = getDefinedRootType(schema, kind);
    const field = type.getFields()[fieldName];
    const operationName = `${fieldName}_${kind}`;
    if (field.args) {
        for (const arg of field.args) {
            const argName = arg.name;
            if (!argNames || argNames.includes(argName)) {
                addOperationVariable(resolveVariable(arg, argName));
            }
        }
    }
    return {
        kind: Kind.OPERATION_DEFINITION,
        operation: kind,
        name: {
            kind: 'Name',
            value: operationName,
        },
        variableDefinitions: [],
        selectionSet: {
            kind: Kind.SELECTION_SET,
            selections: [
                resolveField({
                    type,
                    field,
                    models,
                    firstCall: true,
                    path: [],
                    ancestors: [],
                    ignore,
                    depthLimit,
                    circularReferenceDepth,
                    schema,
                    depth: 0,
                    argNames,
                    selectedFields,
                }),
            ],
        },
    };
}
function resolveSelectionSet({ parent, type, models, firstCall, path, ancestors, ignore, depthLimit, circularReferenceDepth, schema, depth, argNames, selectedFields, }) {
    if (typeof selectedFields === 'boolean' && depth > depthLimit) {
        return;
    }
    if (isUnionType(type)) {
        const types = type.getTypes();
        return {
            kind: Kind.SELECTION_SET,
            selections: types
                .filter(t => !hasCircularRef([...ancestors, t], {
                depth: circularReferenceDepth,
            }))
                .map(t => {
                return {
                    kind: Kind.INLINE_FRAGMENT,
                    typeCondition: {
                        kind: Kind.NAMED_TYPE,
                        name: {
                            kind: Kind.NAME,
                            value: t.name,
                        },
                    },
                    selectionSet: resolveSelectionSet({
                        parent: type,
                        type: t,
                        models,
                        path,
                        ancestors,
                        ignore,
                        depthLimit,
                        circularReferenceDepth,
                        schema,
                        depth,
                        argNames,
                        selectedFields,
                    }),
                };
            })
                .filter(fragmentNode => { var _a, _b; return ((_b = (_a = fragmentNode === null || fragmentNode === void 0 ? void 0 : fragmentNode.selectionSet) === null || _a === void 0 ? void 0 : _a.selections) === null || _b === void 0 ? void 0 : _b.length) > 0; }),
        };
    }
    if (isInterfaceType(type)) {
        const types = Object.values(schema.getTypeMap()).filter((t) => isObjectType(t) && t.getInterfaces().includes(type));
        return {
            kind: Kind.SELECTION_SET,
            selections: types
                .filter(t => !hasCircularRef([...ancestors, t], {
                depth: circularReferenceDepth,
            }))
                .map(t => {
                return {
                    kind: Kind.INLINE_FRAGMENT,
                    typeCondition: {
                        kind: Kind.NAMED_TYPE,
                        name: {
                            kind: Kind.NAME,
                            value: t.name,
                        },
                    },
                    selectionSet: resolveSelectionSet({
                        parent: type,
                        type: t,
                        models,
                        path,
                        ancestors,
                        ignore,
                        depthLimit,
                        circularReferenceDepth,
                        schema,
                        depth,
                        argNames,
                        selectedFields,
                    }),
                };
            })
                .filter(fragmentNode => { var _a, _b; return ((_b = (_a = fragmentNode === null || fragmentNode === void 0 ? void 0 : fragmentNode.selectionSet) === null || _a === void 0 ? void 0 : _a.selections) === null || _b === void 0 ? void 0 : _b.length) > 0; }),
        };
    }
    if (isObjectType(type)) {
        const isIgnored = ignore.includes(type.name) || ignore.includes(`${parent.name}.${path[path.length - 1]}`);
        const isModel = models.includes(type.name);
        if (!firstCall && isModel && !isIgnored) {
            return {
                kind: Kind.SELECTION_SET,
                selections: [
                    {
                        kind: Kind.FIELD,
                        name: {
                            kind: Kind.NAME,
                            value: 'id',
                        },
                    },
                ],
            };
        }
        const fields = type.getFields();
        return {
            kind: Kind.SELECTION_SET,
            selections: Object.keys(fields)
                .filter(fieldName => {
                return !hasCircularRef([...ancestors, getNamedType(fields[fieldName].type)], {
                    depth: circularReferenceDepth,
                });
            })
                .map(fieldName => {
                const selectedSubFields = typeof selectedFields === 'object' ? selectedFields[fieldName] : true;
                if (selectedSubFields) {
                    return resolveField({
                        type: type,
                        field: fields[fieldName],
                        models,
                        path: [...path, fieldName],
                        ancestors,
                        ignore,
                        depthLimit,
                        circularReferenceDepth,
                        schema,
                        depth,
                        argNames,
                        selectedFields: selectedSubFields,
                    });
                }
                return null;
            })
                .filter((f) => {
                var _a, _b;
                if (f == null) {
                    return false;
                }
                else if ('selectionSet' in f) {
                    return !!((_b = (_a = f.selectionSet) === null || _a === void 0 ? void 0 : _a.selections) === null || _b === void 0 ? void 0 : _b.length);
                }
                return true;
            }),
        };
    }
}
function resolveVariable(arg, name) {
    function resolveVariableType(type) {
        if (isListType(type)) {
            return {
                kind: Kind.LIST_TYPE,
                type: resolveVariableType(type.ofType),
            };
        }
        if (isNonNullType(type)) {
            return {
                kind: Kind.NON_NULL_TYPE,
                type: resolveVariableType(type.ofType),
            };
        }
        return {
            kind: Kind.NAMED_TYPE,
            name: {
                kind: Kind.NAME,
                value: type.name,
            },
        };
    }
    return {
        kind: Kind.VARIABLE_DEFINITION,
        variable: {
            kind: Kind.VARIABLE,
            name: {
                kind: Kind.NAME,
                value: name || arg.name,
            },
        },
        type: resolveVariableType(arg.type),
    };
}
function getArgumentName(name, path) {
    return [...path, name].join('_');
}
function resolveField({ type, field, models, firstCall, path, ancestors, ignore, depthLimit, circularReferenceDepth, schema, depth, argNames, selectedFields, }) {
    const namedType = getNamedType(field.type);
    let args = [];
    let removeField = false;
    if (field.args && field.args.length) {
        args = field.args
            .map(arg => {
            const argumentName = getArgumentName(arg.name, path);
            if (argNames && !argNames.includes(argumentName)) {
                if (isNonNullType(arg.type)) {
                    removeField = true;
                }
                return null;
            }
            if (!firstCall) {
                addOperationVariable(resolveVariable(arg, argumentName));
            }
            return {
                kind: Kind.ARGUMENT,
                name: {
                    kind: Kind.NAME,
                    value: arg.name,
                },
                value: {
                    kind: Kind.VARIABLE,
                    name: {
                        kind: Kind.NAME,
                        value: getArgumentName(arg.name, path),
                    },
                },
            };
        })
            .filter(Boolean);
    }
    if (removeField) {
        return null;
    }
    const fieldPath = [...path, field.name];
    const fieldPathStr = fieldPath.join('.');
    let fieldName = field.name;
    if (fieldTypeMap.has(fieldPathStr) && fieldTypeMap.get(fieldPathStr) !== field.type.toString()) {
        fieldName += field.type.toString().replace('!', 'NonNull');
    }
    fieldTypeMap.set(fieldPathStr, field.type.toString());
    if (!isScalarType(namedType) && !isEnumType(namedType)) {
        return {
            kind: Kind.FIELD,
            name: {
                kind: Kind.NAME,
                value: field.name,
            },
            ...(fieldName !== field.name && { alias: { kind: Kind.NAME, value: fieldName } }),
            selectionSet: resolveSelectionSet({
                parent: type,
                type: namedType,
                models,
                firstCall,
                path: fieldPath,
                ancestors: [...ancestors, type],
                ignore,
                depthLimit,
                circularReferenceDepth,
                schema,
                depth: depth + 1,
                argNames,
                selectedFields,
            }) || undefined,
            arguments: args,
        };
    }
    return {
        kind: Kind.FIELD,
        name: {
            kind: Kind.NAME,
            value: field.name,
        },
        ...(fieldName !== field.name && { alias: { kind: Kind.NAME, value: fieldName } }),
        arguments: args,
    };
}
function hasCircularRef(types, config = {
    depth: 1,
}) {
    const type = types[types.length - 1];
    if (isScalarType(type)) {
        return false;
    }
    const size = types.filter(t => t.name === type.name).length;
    return size > config.depth;
}

var MapperKind;
(function (MapperKind) {
    MapperKind["TYPE"] = "MapperKind.TYPE";
    MapperKind["SCALAR_TYPE"] = "MapperKind.SCALAR_TYPE";
    MapperKind["ENUM_TYPE"] = "MapperKind.ENUM_TYPE";
    MapperKind["COMPOSITE_TYPE"] = "MapperKind.COMPOSITE_TYPE";
    MapperKind["OBJECT_TYPE"] = "MapperKind.OBJECT_TYPE";
    MapperKind["INPUT_OBJECT_TYPE"] = "MapperKind.INPUT_OBJECT_TYPE";
    MapperKind["ABSTRACT_TYPE"] = "MapperKind.ABSTRACT_TYPE";
    MapperKind["UNION_TYPE"] = "MapperKind.UNION_TYPE";
    MapperKind["INTERFACE_TYPE"] = "MapperKind.INTERFACE_TYPE";
    MapperKind["ROOT_OBJECT"] = "MapperKind.ROOT_OBJECT";
    MapperKind["QUERY"] = "MapperKind.QUERY";
    MapperKind["MUTATION"] = "MapperKind.MUTATION";
    MapperKind["SUBSCRIPTION"] = "MapperKind.SUBSCRIPTION";
    MapperKind["DIRECTIVE"] = "MapperKind.DIRECTIVE";
    MapperKind["FIELD"] = "MapperKind.FIELD";
    MapperKind["COMPOSITE_FIELD"] = "MapperKind.COMPOSITE_FIELD";
    MapperKind["OBJECT_FIELD"] = "MapperKind.OBJECT_FIELD";
    MapperKind["ROOT_FIELD"] = "MapperKind.ROOT_FIELD";
    MapperKind["QUERY_ROOT_FIELD"] = "MapperKind.QUERY_ROOT_FIELD";
    MapperKind["MUTATION_ROOT_FIELD"] = "MapperKind.MUTATION_ROOT_FIELD";
    MapperKind["SUBSCRIPTION_ROOT_FIELD"] = "MapperKind.SUBSCRIPTION_ROOT_FIELD";
    MapperKind["INTERFACE_FIELD"] = "MapperKind.INTERFACE_FIELD";
    MapperKind["INPUT_OBJECT_FIELD"] = "MapperKind.INPUT_OBJECT_FIELD";
    MapperKind["ARGUMENT"] = "MapperKind.ARGUMENT";
    MapperKind["ENUM_VALUE"] = "MapperKind.ENUM_VALUE";
})(MapperKind || (MapperKind = {}));

function getObjectTypeFromTypeMap(typeMap, type) {
    if (type) {
        const maybeObjectType = typeMap[type.name];
        if (isObjectType(maybeObjectType)) {
            return maybeObjectType;
        }
    }
}

function createNamedStub(name, type) {
    let constructor;
    if (type === 'object') {
        constructor = GraphQLObjectType;
    }
    else if (type === 'interface') {
        constructor = GraphQLInterfaceType;
    }
    else {
        constructor = GraphQLInputObjectType;
    }
    return new constructor({
        name,
        fields: {
            _fake: {
                type: GraphQLString,
            },
        },
    });
}
function createStub(node, type) {
    switch (node.kind) {
        case Kind.LIST_TYPE:
            return new GraphQLList(createStub(node.type, type));
        case Kind.NON_NULL_TYPE:
            return new GraphQLNonNull(createStub(node.type, type));
        default:
            if (type === 'output') {
                return createNamedStub(node.name.value, 'object');
            }
            return createNamedStub(node.name.value, 'input');
    }
}
function isNamedStub(type) {
    if ('getFields' in type) {
        const fields = type.getFields();
        // eslint-disable-next-line no-unreachable-loop
        for (const fieldName in fields) {
            const field = fields[fieldName];
            return field.name === '_fake';
        }
    }
    return false;
}
function getBuiltInForStub(type) {
    switch (type.name) {
        case GraphQLInt.name:
            return GraphQLInt;
        case GraphQLFloat.name:
            return GraphQLFloat;
        case GraphQLString.name:
            return GraphQLString;
        case GraphQLBoolean.name:
            return GraphQLBoolean;
        case GraphQLID.name:
            return GraphQLID;
        default:
            return type;
    }
}

function rewireTypes(originalTypeMap, directives) {
    const referenceTypeMap = Object.create(null);
    for (const typeName in originalTypeMap) {
        referenceTypeMap[typeName] = originalTypeMap[typeName];
    }
    const newTypeMap = Object.create(null);
    for (const typeName in referenceTypeMap) {
        const namedType = referenceTypeMap[typeName];
        if (namedType == null || typeName.startsWith('__')) {
            continue;
        }
        const newName = namedType.name;
        if (newName.startsWith('__')) {
            continue;
        }
        if (newTypeMap[newName] != null) {
            throw new Error(`Duplicate schema type name ${newName}`);
        }
        newTypeMap[newName] = namedType;
    }
    for (const typeName in newTypeMap) {
        newTypeMap[typeName] = rewireNamedType(newTypeMap[typeName]);
    }
    const newDirectives = directives.map(directive => rewireDirective(directive));
    return {
        typeMap: newTypeMap,
        directives: newDirectives,
    };
    function rewireDirective(directive) {
        if (isSpecifiedDirective(directive)) {
            return directive;
        }
        const directiveConfig = directive.toConfig();
        directiveConfig.args = rewireArgs(directiveConfig.args);
        return new GraphQLDirective(directiveConfig);
    }
    function rewireArgs(args) {
        const rewiredArgs = {};
        for (const argName in args) {
            const arg = args[argName];
            const rewiredArgType = rewireType(arg.type);
            if (rewiredArgType != null) {
                arg.type = rewiredArgType;
                rewiredArgs[argName] = arg;
            }
        }
        return rewiredArgs;
    }
    function rewireNamedType(type) {
        if (isObjectType(type)) {
            const config = type.toConfig();
            const newConfig = {
                ...config,
                fields: () => rewireFields(config.fields),
                interfaces: () => rewireNamedTypes(config.interfaces),
            };
            return new GraphQLObjectType(newConfig);
        }
        else if (isInterfaceType(type)) {
            const config = type.toConfig();
            const newConfig = {
                ...config,
                fields: () => rewireFields(config.fields),
            };
            if ('interfaces' in newConfig) {
                newConfig.interfaces = () => rewireNamedTypes(config.interfaces);
            }
            return new GraphQLInterfaceType(newConfig);
        }
        else if (isUnionType(type)) {
            const config = type.toConfig();
            const newConfig = {
                ...config,
                types: () => rewireNamedTypes(config.types),
            };
            return new GraphQLUnionType(newConfig);
        }
        else if (isInputObjectType(type)) {
            const config = type.toConfig();
            const newConfig = {
                ...config,
                fields: () => rewireInputFields(config.fields),
            };
            return new GraphQLInputObjectType(newConfig);
        }
        else if (isEnumType(type)) {
            const enumConfig = type.toConfig();
            return new GraphQLEnumType(enumConfig);
        }
        else if (isScalarType(type)) {
            if (isSpecifiedScalarType(type)) {
                return type;
            }
            const scalarConfig = type.toConfig();
            return new GraphQLScalarType(scalarConfig);
        }
        throw new Error(`Unexpected schema type: ${type}`);
    }
    function rewireFields(fields) {
        const rewiredFields = {};
        for (const fieldName in fields) {
            const field = fields[fieldName];
            const rewiredFieldType = rewireType(field.type);
            if (rewiredFieldType != null && field.args) {
                field.type = rewiredFieldType;
                field.args = rewireArgs(field.args);
                rewiredFields[fieldName] = field;
            }
        }
        return rewiredFields;
    }
    function rewireInputFields(fields) {
        const rewiredFields = {};
        for (const fieldName in fields) {
            const field = fields[fieldName];
            const rewiredFieldType = rewireType(field.type);
            if (rewiredFieldType != null) {
                field.type = rewiredFieldType;
                rewiredFields[fieldName] = field;
            }
        }
        return rewiredFields;
    }
    function rewireNamedTypes(namedTypes) {
        const rewiredTypes = [];
        for (const namedType of namedTypes) {
            const rewiredType = rewireType(namedType);
            if (rewiredType != null) {
                rewiredTypes.push(rewiredType);
            }
        }
        return rewiredTypes;
    }
    function rewireType(type) {
        if (isListType(type)) {
            const rewiredType = rewireType(type.ofType);
            return rewiredType != null ? new GraphQLList(rewiredType) : null;
        }
        else if (isNonNullType(type)) {
            const rewiredType = rewireType(type.ofType);
            return rewiredType != null ? new GraphQLNonNull(rewiredType) : null;
        }
        else if (isNamedType(type)) {
            let rewiredType = referenceTypeMap[type.name];
            if (rewiredType === undefined) {
                rewiredType = isNamedStub(type) ? getBuiltInForStub(type) : rewireNamedType(type);
                newTypeMap[rewiredType.name] = referenceTypeMap[type.name] = rewiredType;
            }
            return rewiredType != null ? newTypeMap[rewiredType.name] : null;
        }
        return null;
    }
}

function transformInputValue(type, value, inputLeafValueTransformer = null, inputObjectValueTransformer = null) {
    if (value == null) {
        return value;
    }
    const nullableType = getNullableType(type);
    if (isLeafType(nullableType)) {
        return inputLeafValueTransformer != null ? inputLeafValueTransformer(nullableType, value) : value;
    }
    else if (isListType(nullableType)) {
        return value.map((listMember) => transformInputValue(nullableType.ofType, listMember, inputLeafValueTransformer, inputObjectValueTransformer));
    }
    else if (isInputObjectType(nullableType)) {
        const fields = nullableType.getFields();
        const newValue = {};
        for (const key in value) {
            const field = fields[key];
            if (field != null) {
                newValue[key] = transformInputValue(field.type, value[key], inputLeafValueTransformer, inputObjectValueTransformer);
            }
        }
        return inputObjectValueTransformer != null ? inputObjectValueTransformer(nullableType, newValue) : newValue;
    }
    // unreachable, no other possible return value
}
function serializeInputValue(type, value) {
    return transformInputValue(type, value, (t, v) => t.serialize(v));
}
function parseInputValue(type, value) {
    return transformInputValue(type, value, (t, v) => t.parseValue(v));
}
function parseInputValueLiteral(type, value) {
    return transformInputValue(type, value, (t, v) => t.parseLiteral(v, {}));
}

function mapSchema(schema, schemaMapper = {}) {
    const newTypeMap = mapArguments(mapFields(mapTypes(mapDefaultValues(mapEnumValues(mapTypes(mapDefaultValues(schema.getTypeMap(), schema, serializeInputValue), schema, schemaMapper, type => isLeafType(type)), schema, schemaMapper), schema, parseInputValue), schema, schemaMapper, type => !isLeafType(type)), schema, schemaMapper), schema, schemaMapper);
    const originalDirectives = schema.getDirectives();
    const newDirectives = mapDirectives(originalDirectives, schema, schemaMapper);
    const { typeMap, directives } = rewireTypes(newTypeMap, newDirectives);
    return new GraphQLSchema({
        ...schema.toConfig(),
        query: getObjectTypeFromTypeMap(typeMap, getObjectTypeFromTypeMap(newTypeMap, schema.getQueryType())),
        mutation: getObjectTypeFromTypeMap(typeMap, getObjectTypeFromTypeMap(newTypeMap, schema.getMutationType())),
        subscription: getObjectTypeFromTypeMap(typeMap, getObjectTypeFromTypeMap(newTypeMap, schema.getSubscriptionType())),
        types: Object.values(typeMap),
        directives,
    });
}
function mapTypes(originalTypeMap, schema, schemaMapper, testFn = () => true) {
    const newTypeMap = {};
    for (const typeName in originalTypeMap) {
        if (!typeName.startsWith('__')) {
            const originalType = originalTypeMap[typeName];
            if (originalType == null || !testFn(originalType)) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const typeMapper = getTypeMapper(schema, schemaMapper, typeName);
            if (typeMapper == null) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const maybeNewType = typeMapper(originalType, schema);
            if (maybeNewType === undefined) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            newTypeMap[typeName] = maybeNewType;
        }
    }
    return newTypeMap;
}
function mapEnumValues(originalTypeMap, schema, schemaMapper) {
    const enumValueMapper = getEnumValueMapper(schemaMapper);
    if (!enumValueMapper) {
        return originalTypeMap;
    }
    return mapTypes(originalTypeMap, schema, {
        [MapperKind.ENUM_TYPE]: type => {
            const config = type.toConfig();
            const originalEnumValueConfigMap = config.values;
            const newEnumValueConfigMap = {};
            for (const externalValue in originalEnumValueConfigMap) {
                const originalEnumValueConfig = originalEnumValueConfigMap[externalValue];
                const mappedEnumValue = enumValueMapper(originalEnumValueConfig, type.name, schema, externalValue);
                if (mappedEnumValue === undefined) {
                    newEnumValueConfigMap[externalValue] = originalEnumValueConfig;
                }
                else if (Array.isArray(mappedEnumValue)) {
                    const [newExternalValue, newEnumValueConfig] = mappedEnumValue;
                    newEnumValueConfigMap[newExternalValue] =
                        newEnumValueConfig === undefined ? originalEnumValueConfig : newEnumValueConfig;
                }
                else if (mappedEnumValue !== null) {
                    newEnumValueConfigMap[externalValue] = mappedEnumValue;
                }
            }
            return correctASTNodes(new GraphQLEnumType({
                ...config,
                values: newEnumValueConfigMap,
            }));
        },
    }, type => isEnumType(type));
}
function mapDefaultValues(originalTypeMap, schema, fn) {
    const newTypeMap = mapArguments(originalTypeMap, schema, {
        [MapperKind.ARGUMENT]: argumentConfig => {
            if (argumentConfig.defaultValue === undefined) {
                return argumentConfig;
            }
            const maybeNewType = getNewType(originalTypeMap, argumentConfig.type);
            if (maybeNewType != null) {
                return {
                    ...argumentConfig,
                    defaultValue: fn(maybeNewType, argumentConfig.defaultValue),
                };
            }
        },
    });
    return mapFields(newTypeMap, schema, {
        [MapperKind.INPUT_OBJECT_FIELD]: inputFieldConfig => {
            if (inputFieldConfig.defaultValue === undefined) {
                return inputFieldConfig;
            }
            const maybeNewType = getNewType(newTypeMap, inputFieldConfig.type);
            if (maybeNewType != null) {
                return {
                    ...inputFieldConfig,
                    defaultValue: fn(maybeNewType, inputFieldConfig.defaultValue),
                };
            }
        },
    });
}
function getNewType(newTypeMap, type) {
    if (isListType(type)) {
        const newType = getNewType(newTypeMap, type.ofType);
        return newType != null ? new GraphQLList(newType) : null;
    }
    else if (isNonNullType(type)) {
        const newType = getNewType(newTypeMap, type.ofType);
        return newType != null ? new GraphQLNonNull(newType) : null;
    }
    else if (isNamedType(type)) {
        const newType = newTypeMap[type.name];
        return newType != null ? newType : null;
    }
    return null;
}
function mapFields(originalTypeMap, schema, schemaMapper) {
    const newTypeMap = {};
    for (const typeName in originalTypeMap) {
        if (!typeName.startsWith('__')) {
            const originalType = originalTypeMap[typeName];
            if (!isObjectType(originalType) && !isInterfaceType(originalType) && !isInputObjectType(originalType)) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const fieldMapper = getFieldMapper(schema, schemaMapper, typeName);
            if (fieldMapper == null) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const config = originalType.toConfig();
            const originalFieldConfigMap = config.fields;
            const newFieldConfigMap = {};
            for (const fieldName in originalFieldConfigMap) {
                const originalFieldConfig = originalFieldConfigMap[fieldName];
                const mappedField = fieldMapper(originalFieldConfig, fieldName, typeName, schema);
                if (mappedField === undefined) {
                    newFieldConfigMap[fieldName] = originalFieldConfig;
                }
                else if (Array.isArray(mappedField)) {
                    const [newFieldName, newFieldConfig] = mappedField;
                    if (newFieldConfig.astNode != null) {
                        newFieldConfig.astNode = {
                            ...newFieldConfig.astNode,
                            name: {
                                ...newFieldConfig.astNode.name,
                                value: newFieldName,
                            },
                        };
                    }
                    newFieldConfigMap[newFieldName] = newFieldConfig === undefined ? originalFieldConfig : newFieldConfig;
                }
                else if (mappedField !== null) {
                    newFieldConfigMap[fieldName] = mappedField;
                }
            }
            if (isObjectType(originalType)) {
                newTypeMap[typeName] = correctASTNodes(new GraphQLObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
            else if (isInterfaceType(originalType)) {
                newTypeMap[typeName] = correctASTNodes(new GraphQLInterfaceType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
            else {
                newTypeMap[typeName] = correctASTNodes(new GraphQLInputObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
        }
    }
    return newTypeMap;
}
function mapArguments(originalTypeMap, schema, schemaMapper) {
    const newTypeMap = {};
    for (const typeName in originalTypeMap) {
        if (!typeName.startsWith('__')) {
            const originalType = originalTypeMap[typeName];
            if (!isObjectType(originalType) && !isInterfaceType(originalType)) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const argumentMapper = getArgumentMapper(schemaMapper);
            if (argumentMapper == null) {
                newTypeMap[typeName] = originalType;
                continue;
            }
            const config = originalType.toConfig();
            const originalFieldConfigMap = config.fields;
            const newFieldConfigMap = {};
            for (const fieldName in originalFieldConfigMap) {
                const originalFieldConfig = originalFieldConfigMap[fieldName];
                const originalArgumentConfigMap = originalFieldConfig.args;
                if (originalArgumentConfigMap == null) {
                    newFieldConfigMap[fieldName] = originalFieldConfig;
                    continue;
                }
                const argumentNames = Object.keys(originalArgumentConfigMap);
                if (!argumentNames.length) {
                    newFieldConfigMap[fieldName] = originalFieldConfig;
                    continue;
                }
                const newArgumentConfigMap = {};
                for (const argumentName of argumentNames) {
                    const originalArgumentConfig = originalArgumentConfigMap[argumentName];
                    const mappedArgument = argumentMapper(originalArgumentConfig, fieldName, typeName, schema);
                    if (mappedArgument === undefined) {
                        newArgumentConfigMap[argumentName] = originalArgumentConfig;
                    }
                    else if (Array.isArray(mappedArgument)) {
                        const [newArgumentName, newArgumentConfig] = mappedArgument;
                        newArgumentConfigMap[newArgumentName] = newArgumentConfig;
                    }
                    else if (mappedArgument !== null) {
                        newArgumentConfigMap[argumentName] = mappedArgument;
                    }
                }
                newFieldConfigMap[fieldName] = {
                    ...originalFieldConfig,
                    args: newArgumentConfigMap,
                };
            }
            if (isObjectType(originalType)) {
                newTypeMap[typeName] = new GraphQLObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                });
            }
            else if (isInterfaceType(originalType)) {
                newTypeMap[typeName] = new GraphQLInterfaceType({
                    ...config,
                    fields: newFieldConfigMap,
                });
            }
            else {
                newTypeMap[typeName] = new GraphQLInputObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                });
            }
        }
    }
    return newTypeMap;
}
function mapDirectives(originalDirectives, schema, schemaMapper) {
    const directiveMapper = getDirectiveMapper(schemaMapper);
    if (directiveMapper == null) {
        return originalDirectives.slice();
    }
    const newDirectives = [];
    for (const directive of originalDirectives) {
        const mappedDirective = directiveMapper(directive, schema);
        if (mappedDirective === undefined) {
            newDirectives.push(directive);
        }
        else if (mappedDirective !== null) {
            newDirectives.push(mappedDirective);
        }
    }
    return newDirectives;
}
function getTypeSpecifiers(schema, typeName) {
    var _a, _b, _c;
    const type = schema.getType(typeName);
    const specifiers = [MapperKind.TYPE];
    if (isObjectType(type)) {
        specifiers.push(MapperKind.COMPOSITE_TYPE, MapperKind.OBJECT_TYPE);
        if (typeName === ((_a = schema.getQueryType()) === null || _a === void 0 ? void 0 : _a.name)) {
            specifiers.push(MapperKind.ROOT_OBJECT, MapperKind.QUERY);
        }
        else if (typeName === ((_b = schema.getMutationType()) === null || _b === void 0 ? void 0 : _b.name)) {
            specifiers.push(MapperKind.ROOT_OBJECT, MapperKind.MUTATION);
        }
        else if (typeName === ((_c = schema.getSubscriptionType()) === null || _c === void 0 ? void 0 : _c.name)) {
            specifiers.push(MapperKind.ROOT_OBJECT, MapperKind.SUBSCRIPTION);
        }
    }
    else if (isInputObjectType(type)) {
        specifiers.push(MapperKind.INPUT_OBJECT_TYPE);
    }
    else if (isInterfaceType(type)) {
        specifiers.push(MapperKind.COMPOSITE_TYPE, MapperKind.ABSTRACT_TYPE, MapperKind.INTERFACE_TYPE);
    }
    else if (isUnionType(type)) {
        specifiers.push(MapperKind.COMPOSITE_TYPE, MapperKind.ABSTRACT_TYPE, MapperKind.UNION_TYPE);
    }
    else if (isEnumType(type)) {
        specifiers.push(MapperKind.ENUM_TYPE);
    }
    else if (isScalarType(type)) {
        specifiers.push(MapperKind.SCALAR_TYPE);
    }
    return specifiers;
}
function getTypeMapper(schema, schemaMapper, typeName) {
    const specifiers = getTypeSpecifiers(schema, typeName);
    let typeMapper;
    const stack = [...specifiers];
    while (!typeMapper && stack.length > 0) {
        // It is safe to use the ! operator here as we check the length.
        const next = stack.pop();
        typeMapper = schemaMapper[next];
    }
    return typeMapper != null ? typeMapper : null;
}
function getFieldSpecifiers(schema, typeName) {
    var _a, _b, _c;
    const type = schema.getType(typeName);
    const specifiers = [MapperKind.FIELD];
    if (isObjectType(type)) {
        specifiers.push(MapperKind.COMPOSITE_FIELD, MapperKind.OBJECT_FIELD);
        if (typeName === ((_a = schema.getQueryType()) === null || _a === void 0 ? void 0 : _a.name)) {
            specifiers.push(MapperKind.ROOT_FIELD, MapperKind.QUERY_ROOT_FIELD);
        }
        else if (typeName === ((_b = schema.getMutationType()) === null || _b === void 0 ? void 0 : _b.name)) {
            specifiers.push(MapperKind.ROOT_FIELD, MapperKind.MUTATION_ROOT_FIELD);
        }
        else if (typeName === ((_c = schema.getSubscriptionType()) === null || _c === void 0 ? void 0 : _c.name)) {
            specifiers.push(MapperKind.ROOT_FIELD, MapperKind.SUBSCRIPTION_ROOT_FIELD);
        }
    }
    else if (isInterfaceType(type)) {
        specifiers.push(MapperKind.COMPOSITE_FIELD, MapperKind.INTERFACE_FIELD);
    }
    else if (isInputObjectType(type)) {
        specifiers.push(MapperKind.INPUT_OBJECT_FIELD);
    }
    return specifiers;
}
function getFieldMapper(schema, schemaMapper, typeName) {
    const specifiers = getFieldSpecifiers(schema, typeName);
    let fieldMapper;
    const stack = [...specifiers];
    while (!fieldMapper && stack.length > 0) {
        // It is safe to use the ! operator here as we check the length.
        const next = stack.pop();
        // TODO: fix this as unknown cast
        fieldMapper = schemaMapper[next];
    }
    return fieldMapper !== null && fieldMapper !== void 0 ? fieldMapper : null;
}
function getArgumentMapper(schemaMapper) {
    const argumentMapper = schemaMapper[MapperKind.ARGUMENT];
    return argumentMapper != null ? argumentMapper : null;
}
function getDirectiveMapper(schemaMapper) {
    const directiveMapper = schemaMapper[MapperKind.DIRECTIVE];
    return directiveMapper != null ? directiveMapper : null;
}
function getEnumValueMapper(schemaMapper) {
    const enumValueMapper = schemaMapper[MapperKind.ENUM_VALUE];
    return enumValueMapper != null ? enumValueMapper : null;
}
function correctASTNodes(type) {
    if (isObjectType(type)) {
        const config = type.toConfig();
        if (config.astNode != null) {
            const fields = [];
            for (const fieldName in config.fields) {
                const fieldConfig = config.fields[fieldName];
                if (fieldConfig.astNode != null) {
                    fields.push(fieldConfig.astNode);
                }
            }
            config.astNode = {
                ...config.astNode,
                kind: Kind.OBJECT_TYPE_DEFINITION,
                fields,
            };
        }
        if (config.extensionASTNodes != null) {
            config.extensionASTNodes = config.extensionASTNodes.map(node => ({
                ...node,
                kind: Kind.OBJECT_TYPE_EXTENSION,
                fields: undefined,
            }));
        }
        return new GraphQLObjectType(config);
    }
    else if (isInterfaceType(type)) {
        const config = type.toConfig();
        if (config.astNode != null) {
            const fields = [];
            for (const fieldName in config.fields) {
                const fieldConfig = config.fields[fieldName];
                if (fieldConfig.astNode != null) {
                    fields.push(fieldConfig.astNode);
                }
            }
            config.astNode = {
                ...config.astNode,
                kind: Kind.INTERFACE_TYPE_DEFINITION,
                fields,
            };
        }
        if (config.extensionASTNodes != null) {
            config.extensionASTNodes = config.extensionASTNodes.map(node => ({
                ...node,
                kind: Kind.INTERFACE_TYPE_EXTENSION,
                fields: undefined,
            }));
        }
        return new GraphQLInterfaceType(config);
    }
    else if (isInputObjectType(type)) {
        const config = type.toConfig();
        if (config.astNode != null) {
            const fields = [];
            for (const fieldName in config.fields) {
                const fieldConfig = config.fields[fieldName];
                if (fieldConfig.astNode != null) {
                    fields.push(fieldConfig.astNode);
                }
            }
            config.astNode = {
                ...config.astNode,
                kind: Kind.INPUT_OBJECT_TYPE_DEFINITION,
                fields,
            };
        }
        if (config.extensionASTNodes != null) {
            config.extensionASTNodes = config.extensionASTNodes.map(node => ({
                ...node,
                kind: Kind.INPUT_OBJECT_TYPE_EXTENSION,
                fields: undefined,
            }));
        }
        return new GraphQLInputObjectType(config);
    }
    else if (isEnumType(type)) {
        const config = type.toConfig();
        if (config.astNode != null) {
            const values = [];
            for (const enumKey in config.values) {
                const enumValueConfig = config.values[enumKey];
                if (enumValueConfig.astNode != null) {
                    values.push(enumValueConfig.astNode);
                }
            }
            config.astNode = {
                ...config.astNode,
                values,
            };
        }
        if (config.extensionASTNodes != null) {
            config.extensionASTNodes = config.extensionASTNodes.map(node => ({
                ...node,
                values: undefined,
            }));
        }
        return new GraphQLEnumType(config);
    }
    else {
        return type;
    }
}

function filterSchema({ schema, typeFilter = () => true, fieldFilter = undefined, rootFieldFilter = undefined, objectFieldFilter = undefined, interfaceFieldFilter = undefined, inputObjectFieldFilter = undefined, argumentFilter = undefined, }) {
    const filteredSchema = mapSchema(schema, {
        [MapperKind.QUERY]: (type) => filterRootFields(type, 'Query', rootFieldFilter, argumentFilter),
        [MapperKind.MUTATION]: (type) => filterRootFields(type, 'Mutation', rootFieldFilter, argumentFilter),
        [MapperKind.SUBSCRIPTION]: (type) => filterRootFields(type, 'Subscription', rootFieldFilter, argumentFilter),
        [MapperKind.OBJECT_TYPE]: (type) => typeFilter(type.name, type)
            ? filterElementFields(GraphQLObjectType, type, objectFieldFilter || fieldFilter, argumentFilter)
            : null,
        [MapperKind.INTERFACE_TYPE]: (type) => typeFilter(type.name, type)
            ? filterElementFields(GraphQLInterfaceType, type, interfaceFieldFilter || fieldFilter, argumentFilter)
            : null,
        [MapperKind.INPUT_OBJECT_TYPE]: (type) => typeFilter(type.name, type)
            ? filterElementFields(GraphQLInputObjectType, type, inputObjectFieldFilter || fieldFilter)
            : null,
        [MapperKind.UNION_TYPE]: (type) => (typeFilter(type.name, type) ? undefined : null),
        [MapperKind.ENUM_TYPE]: (type) => (typeFilter(type.name, type) ? undefined : null),
        [MapperKind.SCALAR_TYPE]: (type) => (typeFilter(type.name, type) ? undefined : null),
    });
    return filteredSchema;
}
function filterRootFields(type, operation, rootFieldFilter, argumentFilter) {
    if (rootFieldFilter || argumentFilter) {
        const config = type.toConfig();
        for (const fieldName in config.fields) {
            const field = config.fields[fieldName];
            if (rootFieldFilter && !rootFieldFilter(operation, fieldName, config.fields[fieldName])) {
                delete config.fields[fieldName];
            }
            else if (argumentFilter && field.args) {
                for (const argName in field.args) {
                    if (!argumentFilter(operation, fieldName, argName, field.args[argName])) {
                        delete field.args[argName];
                    }
                }
            }
        }
        return new GraphQLObjectType(config);
    }
    return type;
}
function filterElementFields(ElementConstructor, type, fieldFilter, argumentFilter) {
    if (fieldFilter || argumentFilter) {
        const config = type.toConfig();
        for (const fieldName in config.fields) {
            const field = config.fields[fieldName];
            if (fieldFilter && !fieldFilter(type.name, fieldName, config.fields[fieldName])) {
                delete config.fields[fieldName];
            }
            else if (argumentFilter && 'args' in field) {
                for (const argName in field.args) {
                    if (!argumentFilter(type.name, fieldName, argName, field.args[argName])) {
                        delete field.args[argName];
                    }
                }
            }
        }
        return new ElementConstructor(config);
    }
}

// Update any references to named schema types that disagree with the named
// types found in schema.getTypeMap().
//
// healSchema and its callers (visitSchema/visitSchemaDirectives) all modify the schema in place.
// Therefore, private variables (such as the stored implementation map and the proper root types)
// are not updated.
//
// If this causes issues, the schema could be more aggressively healed as follows:
//
// healSchema(schema);
// const config = schema.toConfig()
// const healedSchema = new GraphQLSchema({
//   ...config,
//   query: schema.getType('<desired new root query type name>'),
//   mutation: schema.getType('<desired new root mutation type name>'),
//   subscription: schema.getType('<desired new root subscription type name>'),
// });
//
// One can then also -- if necessary --  assign the correct private variables to the initial schema
// as follows:
// Object.assign(schema, healedSchema);
//
// These steps are not taken automatically to preserve backwards compatibility with graphql-tools v4.
// See https://github.com/ardatan/graphql-tools/issues/1462
//
// They were briefly taken in v5, but can now be phased out as they were only required when other
// areas of the codebase were using healSchema and visitSchema more extensively.
//
function healSchema(schema) {
    healTypes(schema.getTypeMap(), schema.getDirectives());
    return schema;
}
function healTypes(originalTypeMap, directives) {
    const actualNamedTypeMap = Object.create(null);
    // If any of the .name properties of the GraphQLNamedType objects in
    // schema.getTypeMap() have changed, the keys of the type map need to
    // be updated accordingly.
    for (const typeName in originalTypeMap) {
        const namedType = originalTypeMap[typeName];
        if (namedType == null || typeName.startsWith('__')) {
            continue;
        }
        const actualName = namedType.name;
        if (actualName.startsWith('__')) {
            continue;
        }
        if (actualName in actualNamedTypeMap) {
            throw new Error(`Duplicate schema type name ${actualName}`);
        }
        actualNamedTypeMap[actualName] = namedType;
        // Note: we are deliberately leaving namedType in the schema by its
        // original name (which might be different from actualName), so that
        // references by that name can be healed.
    }
    // Now add back every named type by its actual name.
    for (const typeName in actualNamedTypeMap) {
        const namedType = actualNamedTypeMap[typeName];
        originalTypeMap[typeName] = namedType;
    }
    // Directive declaration argument types can refer to named types.
    for (const decl of directives) {
        decl.args = decl.args.filter(arg => {
            arg.type = healType(arg.type);
            return arg.type !== null;
        });
    }
    for (const typeName in originalTypeMap) {
        const namedType = originalTypeMap[typeName];
        // Heal all named types, except for dangling references, kept only to redirect.
        if (!typeName.startsWith('__') && typeName in actualNamedTypeMap) {
            if (namedType != null) {
                healNamedType(namedType);
            }
        }
    }
    for (const typeName in originalTypeMap) {
        if (!typeName.startsWith('__') && !(typeName in actualNamedTypeMap)) {
            delete originalTypeMap[typeName];
        }
    }
    function healNamedType(type) {
        if (isObjectType(type)) {
            healFields(type);
            healInterfaces(type);
            return;
        }
        else if (isInterfaceType(type)) {
            healFields(type);
            if ('getInterfaces' in type) {
                healInterfaces(type);
            }
            return;
        }
        else if (isUnionType(type)) {
            healUnderlyingTypes(type);
            return;
        }
        else if (isInputObjectType(type)) {
            healInputFields(type);
            return;
        }
        else if (isLeafType(type)) {
            return;
        }
        throw new Error(`Unexpected schema type: ${type}`);
    }
    function healFields(type) {
        const fieldMap = type.getFields();
        for (const [key, field] of Object.entries(fieldMap)) {
            field.args
                .map(arg => {
                arg.type = healType(arg.type);
                return arg.type === null ? null : arg;
            })
                .filter(Boolean);
            field.type = healType(field.type);
            if (field.type === null) {
                delete fieldMap[key];
            }
        }
    }
    function healInterfaces(type) {
        if ('getInterfaces' in type) {
            const interfaces = type.getInterfaces();
            interfaces.push(...interfaces
                .splice(0)
                .map(iface => healType(iface))
                .filter(Boolean));
        }
    }
    function healInputFields(type) {
        const fieldMap = type.getFields();
        for (const [key, field] of Object.entries(fieldMap)) {
            field.type = healType(field.type);
            if (field.type === null) {
                delete fieldMap[key];
            }
        }
    }
    function healUnderlyingTypes(type) {
        const types = type.getTypes();
        types.push(...types
            .splice(0)
            .map(t => healType(t))
            .filter(Boolean));
    }
    function healType(type) {
        // Unwrap the two known wrapper types
        if (isListType(type)) {
            const healedType = healType(type.ofType);
            return healedType != null ? new GraphQLList(healedType) : null;
        }
        else if (isNonNullType(type)) {
            const healedType = healType(type.ofType);
            return healedType != null ? new GraphQLNonNull(healedType) : null;
        }
        else if (isNamedType(type)) {
            // If a type annotation on a field or an argument or a union member is
            // any `GraphQLNamedType` with a `name`, then it must end up identical
            // to `schema.getType(name)`, since `schema.getTypeMap()` is the source
            // of truth for all named schema types.
            // Note that new types can still be simply added by adding a field, as
            // the official type will be undefined, not null.
            const officialType = originalTypeMap[type.name];
            if (officialType && type !== officialType) {
                return officialType;
            }
        }
        return type;
    }
}

function getResolversFromSchema(schema) {
    var _a, _b;
    const resolvers = Object.create({});
    const typeMap = schema.getTypeMap();
    for (const typeName in typeMap) {
        if (!typeName.startsWith('__')) {
            const type = typeMap[typeName];
            if (isScalarType(type)) {
                if (!isSpecifiedScalarType(type)) {
                    const config = type.toConfig();
                    delete config.astNode; // avoid AST duplication elsewhere
                    resolvers[typeName] = new GraphQLScalarType(config);
                }
            }
            else if (isEnumType(type)) {
                resolvers[typeName] = {};
                const values = type.getValues();
                for (const value of values) {
                    resolvers[typeName][value.name] = value.value;
                }
            }
            else if (isInterfaceType(type)) {
                if (type.resolveType != null) {
                    resolvers[typeName] = {
                        __resolveType: type.resolveType,
                    };
                }
            }
            else if (isUnionType(type)) {
                if (type.resolveType != null) {
                    resolvers[typeName] = {
                        __resolveType: type.resolveType,
                    };
                }
            }
            else if (isObjectType(type)) {
                resolvers[typeName] = {};
                if (type.isTypeOf != null) {
                    resolvers[typeName].__isTypeOf = type.isTypeOf;
                }
                const fields = type.getFields();
                for (const fieldName in fields) {
                    const field = fields[fieldName];
                    if (field.subscribe != null) {
                        resolvers[typeName][fieldName] = resolvers[typeName][fieldName] || {};
                        resolvers[typeName][fieldName].subscribe = field.subscribe;
                    }
                    if (field.resolve != null &&
                        ((_a = field.resolve) === null || _a === void 0 ? void 0 : _a.name) !== 'defaultFieldResolver' &&
                        ((_b = field.resolve) === null || _b === void 0 ? void 0 : _b.name) !== 'defaultMergedResolver') {
                        resolvers[typeName][fieldName] = resolvers[typeName][fieldName] || {};
                        resolvers[typeName][fieldName].resolve = field.resolve;
                    }
                }
            }
        }
    }
    return resolvers;
}

function forEachField(schema, fn) {
    const typeMap = schema.getTypeMap();
    for (const typeName in typeMap) {
        const type = typeMap[typeName];
        // TODO: maybe have an option to include these?
        if (!getNamedType(type).name.startsWith('__') && isObjectType(type)) {
            const fields = type.getFields();
            for (const fieldName in fields) {
                const field = fields[fieldName];
                fn(field, typeName, fieldName);
            }
        }
    }
}

function forEachDefaultValue(schema, fn) {
    const typeMap = schema.getTypeMap();
    for (const typeName in typeMap) {
        const type = typeMap[typeName];
        if (!getNamedType(type).name.startsWith('__')) {
            if (isObjectType(type)) {
                const fields = type.getFields();
                for (const fieldName in fields) {
                    const field = fields[fieldName];
                    for (const arg of field.args) {
                        arg.defaultValue = fn(arg.type, arg.defaultValue);
                    }
                }
            }
            else if (isInputObjectType(type)) {
                const fields = type.getFields();
                for (const fieldName in fields) {
                    const field = fields[fieldName];
                    field.defaultValue = fn(field.type, field.defaultValue);
                }
            }
        }
    }
}

// addTypes uses toConfig to create a new schema with a new or replaced
function addTypes(schema, newTypesOrDirectives) {
    const config = schema.toConfig();
    const originalTypeMap = {};
    for (const type of config.types) {
        originalTypeMap[type.name] = type;
    }
    const originalDirectiveMap = {};
    for (const directive of config.directives) {
        originalDirectiveMap[directive.name] = directive;
    }
    for (const newTypeOrDirective of newTypesOrDirectives) {
        if (isNamedType(newTypeOrDirective)) {
            originalTypeMap[newTypeOrDirective.name] = newTypeOrDirective;
        }
        else if (isDirective(newTypeOrDirective)) {
            originalDirectiveMap[newTypeOrDirective.name] = newTypeOrDirective;
        }
    }
    const { typeMap, directives } = rewireTypes(originalTypeMap, Object.values(originalDirectiveMap));
    return new GraphQLSchema({
        ...config,
        query: getObjectTypeFromTypeMap(typeMap, schema.getQueryType()),
        mutation: getObjectTypeFromTypeMap(typeMap, schema.getMutationType()),
        subscription: getObjectTypeFromTypeMap(typeMap, schema.getSubscriptionType()),
        types: Object.values(typeMap),
        directives,
    });
}

/**
 * Prunes the provided schema, removing unused and empty types
 * @param schema The schema to prune
 * @param options Additional options for removing unused types from the schema
 */
function pruneSchema(schema, options = {}) {
    const pruningContext = {
        schema,
        unusedTypes: Object.create(null),
        implementations: Object.create(null),
    };
    for (const typeName in schema.getTypeMap()) {
        const type = schema.getType(typeName);
        if (type && 'getInterfaces' in type) {
            for (const iface of type.getInterfaces()) {
                const implementations = getImplementations(pruningContext, iface);
                if (implementations == null) {
                    pruningContext.implementations[iface.name] = Object.create(null);
                }
                pruningContext.implementations[iface.name][type.name] = true;
            }
        }
    }
    visitTypes(pruningContext, schema);
    return mapSchema(schema, {
        [MapperKind.TYPE]: (type) => {
            // If we should NOT prune the type, return it immediately as unmodified
            if (options.skipPruning && options.skipPruning(type)) {
                return type;
            }
            if (isObjectType(type) || isInputObjectType(type)) {
                if ((!Object.keys(type.getFields()).length && !options.skipEmptyCompositeTypePruning) ||
                    (pruningContext.unusedTypes[type.name] && !options.skipUnusedTypesPruning)) {
                    return null;
                }
            }
            else if (isUnionType(type)) {
                if ((!type.getTypes().length && !options.skipEmptyUnionPruning) ||
                    (pruningContext.unusedTypes[type.name] && !options.skipUnusedTypesPruning)) {
                    return null;
                }
            }
            else if (isInterfaceType(type)) {
                const implementations = getImplementations(pruningContext, type);
                if ((!Object.keys(type.getFields()).length && !options.skipEmptyCompositeTypePruning) ||
                    (implementations && !Object.keys(implementations).length && !options.skipUnimplementedInterfacesPruning) ||
                    (pruningContext.unusedTypes[type.name] && !options.skipUnusedTypesPruning)) {
                    return null;
                }
            }
            else {
                if (pruningContext.unusedTypes[type.name] && !options.skipUnusedTypesPruning) {
                    return null;
                }
            }
        },
    });
}
function visitOutputType(visitedTypes, pruningContext, type) {
    if (visitedTypes[type.name]) {
        return;
    }
    visitedTypes[type.name] = true;
    pruningContext.unusedTypes[type.name] = false;
    if (isObjectType(type) || isInterfaceType(type)) {
        const fields = type.getFields();
        for (const fieldName in fields) {
            const field = fields[fieldName];
            const namedType = getNamedType(field.type);
            visitOutputType(visitedTypes, pruningContext, namedType);
            for (const arg of field.args) {
                const type = getNamedType(arg.type);
                visitInputType(visitedTypes, pruningContext, type);
            }
        }
        if (isInterfaceType(type)) {
            const implementations = getImplementations(pruningContext, type);
            if (implementations) {
                for (const typeName in implementations) {
                    visitOutputType(visitedTypes, pruningContext, pruningContext.schema.getType(typeName));
                }
            }
        }
        if ('getInterfaces' in type) {
            for (const iFace of type.getInterfaces()) {
                visitOutputType(visitedTypes, pruningContext, iFace);
            }
        }
    }
    else if (isUnionType(type)) {
        const types = type.getTypes();
        for (const type of types) {
            visitOutputType(visitedTypes, pruningContext, type);
        }
    }
}
/**
 * Get the implementations of an interface. May return undefined.
 */
function getImplementations(pruningContext, type) {
    return pruningContext.implementations[type.name];
}
function visitInputType(visitedTypes, pruningContext, type) {
    if (visitedTypes[type.name]) {
        return;
    }
    pruningContext.unusedTypes[type.name] = false;
    visitedTypes[type.name] = true;
    if (isInputObjectType(type)) {
        const fields = type.getFields();
        for (const fieldName in fields) {
            const field = fields[fieldName];
            const namedType = getNamedType(field.type);
            visitInputType(visitedTypes, pruningContext, namedType);
        }
    }
}
function visitTypes(pruningContext, schema) {
    for (const typeName in schema.getTypeMap()) {
        if (!typeName.startsWith('__')) {
            pruningContext.unusedTypes[typeName] = true;
        }
    }
    const visitedTypes = Object.create(null);
    const rootTypes = getRootTypes(schema);
    for (const rootType of rootTypes) {
        visitOutputType(visitedTypes, pruningContext, rootType);
    }
    for (const directive of schema.getDirectives()) {
        for (const arg of directive.args) {
            const type = getNamedType(arg.type);
            visitInputType(visitedTypes, pruningContext, type);
        }
    }
}

// eslint-disable-next-line @typescript-eslint/ban-types
function mergeDeep(sources, respectPrototype = false) {
    const target = sources[0] || {};
    const output = {};
    if (respectPrototype) {
        Object.setPrototypeOf(output, Object.create(Object.getPrototypeOf(target)));
    }
    for (const source of sources) {
        if (isObject(target) && isObject(source)) {
            if (respectPrototype) {
                const outputPrototype = Object.getPrototypeOf(output);
                const sourcePrototype = Object.getPrototypeOf(source);
                if (sourcePrototype) {
                    for (const key of Object.getOwnPropertyNames(sourcePrototype)) {
                        const descriptor = Object.getOwnPropertyDescriptor(sourcePrototype, key);
                        if (isSome(descriptor)) {
                            Object.defineProperty(outputPrototype, key, descriptor);
                        }
                    }
                }
            }
            for (const key in source) {
                if (isObject(source[key])) {
                    if (!(key in output)) {
                        Object.assign(output, { [key]: source[key] });
                    }
                    else {
                        output[key] = mergeDeep([output[key], source[key]], respectPrototype);
                    }
                }
                else {
                    Object.assign(output, { [key]: source[key] });
                }
            }
        }
    }
    return output;
}
function isObject(item) {
    return item && typeof item === 'object' && !Array.isArray(item);
}

function parseSelectionSet(selectionSet, options) {
    const query = parse(selectionSet, options).definitions[0];
    return query.selectionSet;
}

/**
 * Get the key under which the result of this resolver will be placed in the response JSON. Basically, just
 * resolves aliases.
 * @param info The info argument to the resolver.
 */
function getResponseKeyFromInfo(info) {
    return info.fieldNodes[0].alias != null ? info.fieldNodes[0].alias.value : info.fieldName;
}

function appendObjectFields(schema, typeName, additionalFields) {
    if (schema.getType(typeName) == null) {
        return addTypes(schema, [
            new GraphQLObjectType({
                name: typeName,
                fields: additionalFields,
            }),
        ]);
    }
    return mapSchema(schema, {
        [MapperKind.OBJECT_TYPE]: type => {
            if (type.name === typeName) {
                const config = type.toConfig();
                const originalFieldConfigMap = config.fields;
                const newFieldConfigMap = {};
                for (const fieldName in originalFieldConfigMap) {
                    newFieldConfigMap[fieldName] = originalFieldConfigMap[fieldName];
                }
                for (const fieldName in additionalFields) {
                    newFieldConfigMap[fieldName] = additionalFields[fieldName];
                }
                return correctASTNodes(new GraphQLObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
        },
    });
}
function removeObjectFields(schema, typeName, testFn) {
    const removedFields = {};
    const newSchema = mapSchema(schema, {
        [MapperKind.OBJECT_TYPE]: type => {
            if (type.name === typeName) {
                const config = type.toConfig();
                const originalFieldConfigMap = config.fields;
                const newFieldConfigMap = {};
                for (const fieldName in originalFieldConfigMap) {
                    const originalFieldConfig = originalFieldConfigMap[fieldName];
                    if (testFn(fieldName, originalFieldConfig)) {
                        removedFields[fieldName] = originalFieldConfig;
                    }
                    else {
                        newFieldConfigMap[fieldName] = originalFieldConfig;
                    }
                }
                return correctASTNodes(new GraphQLObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
        },
    });
    return [newSchema, removedFields];
}
function selectObjectFields(schema, typeName, testFn) {
    const selectedFields = {};
    mapSchema(schema, {
        [MapperKind.OBJECT_TYPE]: type => {
            if (type.name === typeName) {
                const config = type.toConfig();
                const originalFieldConfigMap = config.fields;
                for (const fieldName in originalFieldConfigMap) {
                    const originalFieldConfig = originalFieldConfigMap[fieldName];
                    if (testFn(fieldName, originalFieldConfig)) {
                        selectedFields[fieldName] = originalFieldConfig;
                    }
                }
            }
            return undefined;
        },
    });
    return selectedFields;
}
function modifyObjectFields(schema, typeName, testFn, newFields) {
    const removedFields = {};
    const newSchema = mapSchema(schema, {
        [MapperKind.OBJECT_TYPE]: type => {
            if (type.name === typeName) {
                const config = type.toConfig();
                const originalFieldConfigMap = config.fields;
                const newFieldConfigMap = {};
                for (const fieldName in originalFieldConfigMap) {
                    const originalFieldConfig = originalFieldConfigMap[fieldName];
                    if (testFn(fieldName, originalFieldConfig)) {
                        removedFields[fieldName] = originalFieldConfig;
                    }
                    else {
                        newFieldConfigMap[fieldName] = originalFieldConfig;
                    }
                }
                for (const fieldName in newFields) {
                    const fieldConfig = newFields[fieldName];
                    newFieldConfigMap[fieldName] = fieldConfig;
                }
                return correctASTNodes(new GraphQLObjectType({
                    ...config,
                    fields: newFieldConfigMap,
                }));
            }
        },
    });
    return [newSchema, removedFields];
}

function renameType(type, newTypeName) {
    if (isObjectType(type)) {
        return new GraphQLObjectType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    else if (isInterfaceType(type)) {
        return new GraphQLInterfaceType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    else if (isUnionType(type)) {
        return new GraphQLUnionType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    else if (isInputObjectType(type)) {
        return new GraphQLInputObjectType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    else if (isEnumType(type)) {
        return new GraphQLEnumType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    else if (isScalarType(type)) {
        return new GraphQLScalarType({
            ...type.toConfig(),
            name: newTypeName,
            astNode: type.astNode == null
                ? type.astNode
                : {
                    ...type.astNode,
                    name: {
                        ...type.astNode.name,
                        value: newTypeName,
                    },
                },
            extensionASTNodes: type.extensionASTNodes == null
                ? type.extensionASTNodes
                : type.extensionASTNodes.map(node => ({
                    ...node,
                    name: {
                        ...node.name,
                        value: newTypeName,
                    },
                })),
        });
    }
    throw new Error(`Unknown type ${type}.`);
}

/**
 * Given an AsyncIterable and a callback function, return an AsyncIterator
 * which produces values mapped via calling the callback function.
 */
function mapAsyncIterator(iterator, callback, rejectCallback) {
    let $return;
    let abruptClose;
    if (typeof iterator.return === 'function') {
        $return = iterator.return;
        abruptClose = (error) => {
            const rethrow = () => Promise.reject(error);
            return $return.call(iterator).then(rethrow, rethrow);
        };
    }
    function mapResult(result) {
        return result.done ? result : asyncMapValue(result.value, callback).then(iteratorResult, abruptClose);
    }
    let mapReject;
    if (rejectCallback) {
        // Capture rejectCallback to ensure it cannot be null.
        const reject = rejectCallback;
        mapReject = (error) => asyncMapValue(error, reject).then(iteratorResult, abruptClose);
    }
    return {
        next() {
            return iterator.next().then(mapResult, mapReject);
        },
        return() {
            return $return
                ? $return.call(iterator).then(mapResult, mapReject)
                : Promise.resolve({ value: undefined, done: true });
        },
        throw(error) {
            if (typeof iterator.throw === 'function') {
                return iterator.throw(error).then(mapResult, mapReject);
            }
            return Promise.reject(error).catch(abruptClose);
        },
        [Symbol.asyncIterator]() {
            return this;
        },
    };
}
function asyncMapValue(value, callback) {
    return new Promise(resolve => resolve(callback(value)));
}
function iteratorResult(value) {
    return { value, done: false };
}

function updateArgument(argumentNodes, variableDefinitionsMap, variableValues, argName, varName, type, value) {
    argumentNodes[argName] = {
        kind: Kind.ARGUMENT,
        name: {
            kind: Kind.NAME,
            value: argName,
        },
        value: {
            kind: Kind.VARIABLE,
            name: {
                kind: Kind.NAME,
                value: varName,
            },
        },
    };
    variableDefinitionsMap[varName] = {
        kind: Kind.VARIABLE_DEFINITION,
        variable: {
            kind: Kind.VARIABLE,
            name: {
                kind: Kind.NAME,
                value: varName,
            },
        },
        type: astFromType(type),
    };
    if (value !== undefined) {
        variableValues[varName] = value;
        return;
    }
    // including the variable in the map with value of `undefined`
    // will actually be translated by graphql-js into `null`
    // see https://github.com/graphql/graphql-js/issues/2533
    if (varName in variableValues) {
        delete variableValues[varName];
    }
}
function createVariableNameGenerator(variableDefinitionMap) {
    let varCounter = 0;
    return (argName) => {
        let varName;
        do {
            varName = `_v${(varCounter++).toString()}_${argName}`;
        } while (varName in variableDefinitionMap);
        return varName;
    };
}

function implementsAbstractType(schema, typeA, typeB) {
    if (typeB == null || typeA == null) {
        return false;
    }
    else if (typeA === typeB) {
        return true;
    }
    else if (isCompositeType(typeA) && isCompositeType(typeB)) {
        return doTypesOverlap(schema, typeA, typeB);
    }
    return false;
}

function relocatedError(originalError, path) {
    return new GraphQLError(originalError.message, originalError.nodes, originalError.source, originalError.positions, path === null ? undefined : path === undefined ? originalError.path : path, originalError.originalError, originalError.extensions);
}

function observableToAsyncIterable(observable) {
    const pullQueue = [];
    const pushQueue = [];
    let listening = true;
    const pushValue = (value) => {
        if (pullQueue.length !== 0) {
            // It is safe to use the ! operator here as we check the length.
            pullQueue.shift()({ value, done: false });
        }
        else {
            pushQueue.push({ value, done: false });
        }
    };
    const pushError = (error) => {
        if (pullQueue.length !== 0) {
            // It is safe to use the ! operator here as we check the length.
            pullQueue.shift()({ value: { errors: [error] }, done: false });
        }
        else {
            pushQueue.push({ value: { errors: [error] }, done: false });
        }
    };
    const pushDone = () => {
        if (pullQueue.length !== 0) {
            // It is safe to use the ! operator here as we check the length.
            pullQueue.shift()({ done: true });
        }
        else {
            pushQueue.push({ done: true });
        }
    };
    const pullValue = () => new Promise(resolve => {
        if (pushQueue.length !== 0) {
            const element = pushQueue.shift();
            // either {value: {errors: [...]}} or {value: ...}
            resolve(element);
        }
        else {
            pullQueue.push(resolve);
        }
    });
    const subscription = observable.subscribe({
        next(value) {
            pushValue(value);
        },
        error(err) {
            pushError(err);
        },
        complete() {
            pushDone();
        },
    });
    const emptyQueue = () => {
        if (listening) {
            listening = false;
            subscription.unsubscribe();
            for (const resolve of pullQueue) {
                resolve({ value: undefined, done: true });
            }
            pullQueue.length = 0;
            pushQueue.length = 0;
        }
    };
    return {
        next() {
            // return is a defined method, so it is safe to call it.
            return listening ? pullValue() : this.return();
        },
        return() {
            emptyQueue();
            return Promise.resolve({ value: undefined, done: true });
        },
        throw(error) {
            emptyQueue();
            return Promise.reject(error);
        },
        [Symbol.asyncIterator]() {
            return this;
        },
    };
}

function visitData(data, enter, leave) {
    if (Array.isArray(data)) {
        return data.map(value => visitData(value, enter, leave));
    }
    else if (typeof data === 'object') {
        const newData = enter != null ? enter(data) : data;
        if (newData != null) {
            for (const key in newData) {
                const value = newData[key];
                newData[key] = visitData(value, enter, leave);
            }
        }
        return leave != null ? leave(newData) : newData;
    }
    return data;
}
function visitErrors(errors, visitor) {
    return errors.map(error => visitor(error));
}
function visitResult(result, request, schema, resultVisitorMap, errorVisitorMap) {
    const partialExecutionContext = {
        schema,
        fragments: request.document.definitions.reduce((acc, def) => {
            if (def.kind === Kind.FRAGMENT_DEFINITION) {
                acc[def.name.value] = def;
            }
            return acc;
        }, {}),
        variableValues: request.variables,
    };
    const errorInfo = {
        segmentInfoMap: new Map(),
        unpathedErrors: new Set(),
    };
    const data = result.data;
    const errors = result.errors;
    const visitingErrors = errors != null && errorVisitorMap != null;
    const operationDocumentNode = getOperationAST(request.document, undefined);
    if (data != null && operationDocumentNode != null) {
        result.data = visitRoot(data, operationDocumentNode, partialExecutionContext, resultVisitorMap, visitingErrors ? errors : undefined, errorInfo);
    }
    if (errors != null && errorVisitorMap) {
        result.errors = visitErrorsByType(errors, errorVisitorMap, errorInfo);
    }
    return result;
}
function visitErrorsByType(errors, errorVisitorMap, errorInfo) {
    const segmentInfoMap = errorInfo.segmentInfoMap;
    const unpathedErrors = errorInfo.unpathedErrors;
    const unpathedErrorVisitor = errorVisitorMap['__unpathed'];
    return errors.map(originalError => {
        const pathSegmentsInfo = segmentInfoMap.get(originalError);
        const newError = pathSegmentsInfo == null
            ? originalError
            : pathSegmentsInfo.reduceRight((acc, segmentInfo) => {
                const typeName = segmentInfo.type.name;
                const typeVisitorMap = errorVisitorMap[typeName];
                if (typeVisitorMap == null) {
                    return acc;
                }
                const errorVisitor = typeVisitorMap[segmentInfo.fieldName];
                return errorVisitor == null ? acc : errorVisitor(acc, segmentInfo.pathIndex);
            }, originalError);
        if (unpathedErrorVisitor && unpathedErrors.has(originalError)) {
            return unpathedErrorVisitor(newError);
        }
        return newError;
    });
}
function visitRoot(root, operation, exeContext, resultVisitorMap, errors, errorInfo) {
    const operationRootType = getOperationRootType(exeContext.schema, operation);
    const collectedFields = collectFields(exeContext, operationRootType, operation.selectionSet, Object.create(null), Object.create(null));
    return visitObjectValue(root, operationRootType, collectedFields, exeContext, resultVisitorMap, 0, errors, errorInfo);
}
function visitObjectValue(object, type, fieldNodeMap, exeContext, resultVisitorMap, pathIndex, errors, errorInfo) {
    const fieldMap = type.getFields();
    const typeVisitorMap = resultVisitorMap === null || resultVisitorMap === void 0 ? void 0 : resultVisitorMap[type.name];
    const enterObject = typeVisitorMap === null || typeVisitorMap === void 0 ? void 0 : typeVisitorMap.__enter;
    const newObject = enterObject != null ? enterObject(object) : object;
    let sortedErrors;
    let errorMap = null;
    if (errors != null) {
        sortedErrors = sortErrorsByPathSegment(errors, pathIndex);
        errorMap = sortedErrors.errorMap;
        for (const error of sortedErrors.unpathedErrors) {
            errorInfo.unpathedErrors.add(error);
        }
    }
    for (const responseKey in fieldNodeMap) {
        const subFieldNodes = fieldNodeMap[responseKey];
        const fieldName = subFieldNodes[0].name.value;
        const fieldType = fieldName === '__typename' ? TypeNameMetaFieldDef.type : fieldMap[fieldName].type;
        const newPathIndex = pathIndex + 1;
        let fieldErrors;
        if (errorMap) {
            fieldErrors = errorMap[responseKey];
            if (fieldErrors != null) {
                delete errorMap[responseKey];
            }
            addPathSegmentInfo(type, fieldName, newPathIndex, fieldErrors, errorInfo);
        }
        const newValue = visitFieldValue(object[responseKey], fieldType, subFieldNodes, exeContext, resultVisitorMap, newPathIndex, fieldErrors, errorInfo);
        updateObject(newObject, responseKey, newValue, typeVisitorMap, fieldName);
    }
    const oldTypename = newObject.__typename;
    if (oldTypename != null) {
        updateObject(newObject, '__typename', oldTypename, typeVisitorMap, '__typename');
    }
    if (errorMap) {
        for (const errors of Object.values(errorMap)) {
            for (const error of errors) {
                errorInfo.unpathedErrors.add(error);
            }
        }
    }
    const leaveObject = typeVisitorMap === null || typeVisitorMap === void 0 ? void 0 : typeVisitorMap.__leave;
    return leaveObject != null ? leaveObject(newObject) : newObject;
}
function updateObject(object, responseKey, newValue, typeVisitorMap, fieldName) {
    if (typeVisitorMap == null) {
        object[responseKey] = newValue;
        return;
    }
    const fieldVisitor = typeVisitorMap[fieldName];
    if (fieldVisitor == null) {
        object[responseKey] = newValue;
        return;
    }
    const visitedValue = fieldVisitor(newValue);
    if (visitedValue === undefined) {
        delete object[responseKey];
        return;
    }
    object[responseKey] = visitedValue;
}
function visitListValue(list, returnType, fieldNodes, exeContext, resultVisitorMap, pathIndex, errors, errorInfo) {
    return list.map(listMember => visitFieldValue(listMember, returnType, fieldNodes, exeContext, resultVisitorMap, pathIndex + 1, errors, errorInfo));
}
function visitFieldValue(value, returnType, fieldNodes, exeContext, resultVisitorMap, pathIndex, errors = [], errorInfo) {
    if (value == null) {
        return value;
    }
    const nullableType = getNullableType(returnType);
    if (isListType(nullableType)) {
        return visitListValue(value, nullableType.ofType, fieldNodes, exeContext, resultVisitorMap, pathIndex, errors, errorInfo);
    }
    else if (isAbstractType(nullableType)) {
        const finalType = exeContext.schema.getType(value.__typename);
        const collectedFields = collectSubFields(exeContext, finalType, fieldNodes);
        return visitObjectValue(value, finalType, collectedFields, exeContext, resultVisitorMap, pathIndex, errors, errorInfo);
    }
    else if (isObjectType(nullableType)) {
        const collectedFields = collectSubFields(exeContext, nullableType, fieldNodes);
        return visitObjectValue(value, nullableType, collectedFields, exeContext, resultVisitorMap, pathIndex, errors, errorInfo);
    }
    const typeVisitorMap = resultVisitorMap === null || resultVisitorMap === void 0 ? void 0 : resultVisitorMap[nullableType.name];
    if (typeVisitorMap == null) {
        return value;
    }
    const visitedValue = typeVisitorMap(value);
    return visitedValue === undefined ? value : visitedValue;
}
function sortErrorsByPathSegment(errors, pathIndex) {
    var _a;
    const errorMap = Object.create(null);
    const unpathedErrors = new Set();
    for (const error of errors) {
        const pathSegment = (_a = error.path) === null || _a === void 0 ? void 0 : _a[pathIndex];
        if (pathSegment == null) {
            unpathedErrors.add(error);
            continue;
        }
        if (pathSegment in errorMap) {
            errorMap[pathSegment].push(error);
        }
        else {
            errorMap[pathSegment] = [error];
        }
    }
    return {
        errorMap,
        unpathedErrors,
    };
}
function addPathSegmentInfo(type, fieldName, pathIndex, errors = [], errorInfo) {
    for (const error of errors) {
        const segmentInfo = {
            type,
            fieldName,
            pathIndex,
        };
        const pathSegmentsInfo = errorInfo.segmentInfoMap.get(error);
        if (pathSegmentsInfo == null) {
            errorInfo.segmentInfoMap.set(error, [segmentInfo]);
        }
        else {
            pathSegmentsInfo.push(segmentInfo);
        }
    }
}
function collectSubFields(exeContext, type, fieldNodes) {
    let subFieldNodes = Object.create(null);
    const visitedFragmentNames = Object.create(null);
    for (const fieldNode of fieldNodes) {
        if (fieldNode.selectionSet) {
            subFieldNodes = collectFields(exeContext, type, fieldNode.selectionSet, subFieldNodes, visitedFragmentNames);
        }
    }
    return subFieldNodes;
}

function valueMatchesCriteria(value, criteria) {
    if (value == null) {
        return value === criteria;
    }
    else if (Array.isArray(value)) {
        return Array.isArray(criteria) && value.every((val, index) => valueMatchesCriteria(val, criteria[index]));
    }
    else if (typeof value === 'object') {
        return (typeof criteria === 'object' &&
            criteria &&
            Object.keys(criteria).every(propertyName => valueMatchesCriteria(value[propertyName], criteria[propertyName])));
    }
    else if (criteria instanceof RegExp) {
        return criteria.test(value);
    }
    return value === criteria;
}

function isAsyncIterable(value) {
    return typeof value === 'object' && value != null && Symbol.asyncIterator in value;
}

function isDocumentNode(object) {
    return object && typeof object === 'object' && 'kind' in object && object.kind === Kind.DOCUMENT;
}

function withCancel(asyncIteratorLike, onCancel) {
    const asyncIterator = asyncIteratorLike[Symbol.asyncIterator]();
    if (!asyncIterator.return) {
        asyncIterator.return = () => Promise.resolve({ value: undefined, done: true });
    }
    const savedReturn = asyncIterator.return.bind(asyncIterator);
    asyncIterator.return = () => {
        onCancel();
        return savedReturn();
    };
    return asyncIterator;
}

export { AggregateErrorImpl as AggregateError, MapperKind, addTypes, appendObjectFields, asArray, assertSome, astFromArg, astFromDirective, astFromEnumType, astFromEnumValue, astFromField, astFromInputField, astFromInputObjectType, astFromInterfaceType, astFromObjectType, astFromScalarType, astFromSchema, astFromUnionType, astFromValueUntyped, buildOperationNodeForField, checkValidationErrors, compareNodes, compareStrings, correctASTNodes, createNamedStub, createSchemaDefinition, createStub, createVariableNameGenerator, filterSchema, fixSchemaAst, forEachDefaultValue, forEachField, getArgumentValues, getBuiltInForStub, getDefinedRootType, getDeprecatableDirectiveNodes, getDirective, getDirectiveInExtensions, getDirectiveNodes, getDirectives, getDirectivesInExtensions, getDocumentNodeFromSchema, getFieldsWithDirectives, getImplementingTypes, getLeadingCommentBlock, getResolversFromSchema, getResponseKeyFromInfo, getRootTypeMap, getRootTypeNames, getRootTypes, getUserTypesFromSchema, healSchema, healTypes, implementsAbstractType, isAsyncIterable, isDescribable, isDocumentNode, isDocumentString, isEqual, isNamedStub, isNotEqual, isSome, isValidPath, makeDeprecatedDirective, makeDirectiveNode, makeDirectiveNodes, mapAsyncIterator, mapSchema, mergeDeep, modifyObjectFields, nodeToString, observableToAsyncIterable, parseGraphQLJSON, parseGraphQLSDL, parseInputValue, parseInputValueLiteral, parseSelectionSet, printSchemaWithDirectives, pruneSchema, relocatedError, removeObjectFields, renameType, rewireTypes, selectObjectFields, serializeInputValue, transformCommentsToDescriptions, transformInputValue, updateArgument, validateGraphQlDocuments, valueMatchesCriteria, visitData, visitErrors, visitResult, withCancel };
