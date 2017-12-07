/*
    $ ./node_modules/.bin/webpack --config webpack.config.js --watch
*/

const path = require("path")
const webpack = require('webpack')
const BundleTracker = require('webpack-bundle-tracker')


module.exports = {
    context: __dirname,

    entry: {
        main: './static/js/main.js'
    },

    output: {
        path: path.resolve('./static/bundles/'),
        filename: "[name]-[hash].js",
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),

        new webpack.ProvidePlugin({
            $: 'jquery',
            'window.$': 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
        })
    ],

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['es2015']
                    }
                }
            },
            { test: /\.css$/, loader: 'style-loader!css-loader' },
            { test: /\.svg$/, loader: 'url-loader?mimetype=image/svg+xml' },
            { test: /\.woff$/, loader: 'url-loader?mimetype=application/font-woff' },
            { test: /\.woff2$/, loader: 'url-loader?mimetype=application/font-woff' },
            { test: /\.eot$/, loader: 'url-loader?mimetype=application/font-woff' },
            { test: /\.ttf$/, loader: 'url-loader?mimetype=application/font-woff' }
        ]
    },

    resolve: {
        alias: {
            'vue': path.resolve('./node_modules/vue/dist/vue.js'),
        }
    },
}
