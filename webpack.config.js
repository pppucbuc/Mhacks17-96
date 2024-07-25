const path = require("path");


module.exports = {
    mode: 'development',
    entry: path.resolve(__dirname, './pj/js/index.js'),  // Your main JS file
    output: {
      filename: 'bundle.js',
      path: path.resolve(__dirname, "pj/static/js/"),  // Output folder
    },
    module: {
      rules: [
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
        extensions: ['.js', '.jsx'], // Automatically resolve these extensions
      },
  };
  