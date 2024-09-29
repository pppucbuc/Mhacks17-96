const path = require("path");


module.exports = {
    mode: 'development',
    entry: path.resolve(__dirname, './pj/js/index.jsx'),  // Your main JS file
    output: {
      filename: 'bundle.js',
      path: path.resolve(__dirname, "pj/static/js/"),  // Output folder
      publicPath: 'static/js/',
    },
    module: {
      rules: [
        {
          test: /\.wasm$/,
          type: 'asset/resource',  //'asset/resource', //'webassembly/async'
        },
        {
            test: /\.jsx?$/, // Match both .js and .jsx files
            exclude: /node_modules/,
            use: {
              loader: 'babel-loader',
              options: {
                presets: ['@babel/preset-env', '@babel/preset-react'],
              }
            }
          },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
        },
  
      ],
    },
    
    resolve: {
        extensions: ['.js', '.jsx','.wasm'], // Automatically resolve these extensions
      },
    experiments: {
      asyncWebAssembly: true,
    },
    devServer: {
      contentBase: path.resolve(__dirname, 'static/js'),
      compress: true,
      port: 8000,
    },

  };
  