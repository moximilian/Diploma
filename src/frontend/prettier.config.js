/** @type {import("prettier").Options} */
// https://prettier.io/docs/en/options.html#print-width
const config = {
    arrowParens: 'avoid', // parentheses around a single parameter of an arrow function
    bracketSpacing: true, // spacing between brackets in object literals
    endOfLine: 'lf', // line endings
    htmlWhitespaceSensitivity: 'css', // format HTML taking whitespace into account
    insertPragma: false, // insert a special comment at the beginning of the file
    jsxBracketSameLine: false, // where to put the closing > of a multi‑line JSX element
    jsxSingleQuote: false, // use single quotes instead of double quotes in JSX
    printWidth: 100, // at which position to wrap lines
    proseWrap: 'preserve', // how to handle markdown files
    quoteProps: 'as-needed', // object properties in quotes or unquoted
    requirePragma: false, // format only files with a special comment at the top
    semi: false, // semicolons at the end of statements
    singleQuote: true, // use single quotes instead of double quotes
    tabWidth: 4, // replace tabs with 4 spaces
    trailingComma: 'es5', // trailing commas in objects and arrays
    useTabs: false, // use tabs for indentation
    vueIndentScriptAndStyle: false, // indentation inside <script> and <style> in Vue files
    embeddedLanguageFormatting: 'auto', // format embedded code
}

module.exports = config