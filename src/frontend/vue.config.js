// @ts-check
const { defineConfig } = require('@vue/cli-service')
const path = require('path')

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

    // filenameHashing: false, 

    chainWebpack: config => {
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
