const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');
const webpack = require('webpack')


module.exports = {
    mode: 'production',
    entry: {
        'url-resolver.js': './index.js',
        'url-resolver.min.js': './index.js',
    },
    target: 'web',
    module: {
        rules: [{
            test: /\.js$/,
            use: {
                loader: 'babel-loader',
            }
        }]
    },
    output: {
        path: path.resolve(__dirname, 'django_reverse_js/templates/django_reverse_js'),
        filename: '[name]',
        library: {
            name: 'resolverFactory',
            type: 'var'
        }
    },
    optimization: {
        minimizer: [
            new TerserPlugin({
                parallel: true,
                include: /\.min/,
                terserOptions: {
                    compress: false,
                    mangle: false,
                }
            })
        ],
        minimize: true,
    }
};
