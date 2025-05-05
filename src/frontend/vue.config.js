// @ts-check
const { defineConfig } = require('@vue/cli-service')
const path = require('path')

const buildList = (process.env.VUE_APP_BUILD_LIST || '').split(', ')

module.exports = defineConfig({
    transpileDependencies: true,
    productionSourceMap: false, 
    publicPath: process.env.BASE_URL || '/',
    pages: {
        index: {
            entry: 'src/main.js',
        }
    },
    configureWebpack: {
        resolve: {
            alias: {
                '@': path.resolve(__dirname, 'src'),
            },
        },
    },

    // Хэши в именах файлов сборки
    // filenameHashing: false, // false для отключения

    chainWebpack: config => {
        // set environment variables
        config.plugin('define').tap(definitions => {
            Object.assign(definitions[0], {
                __VUE_I18N_FULL_INSTALL__: JSON.stringify(true),
                __INTLIFY_PROD_DEVTOOLS__: JSON.stringify(false),
                __VUE_I18N_LEGACY_API__: JSON.stringify(false),
            })

            return definitions
        })
    },
})
