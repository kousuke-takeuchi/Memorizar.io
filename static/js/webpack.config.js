// development: 開発時のファイル出力のモード(最適化より時間短縮,エラー表示などを優先)
// production: 本番時のファイル出力のモード(最適化されて出力される)
const MODE = "development";
// ソースマップの利用有無(productionのときはソースマップを利用しない)
const enabledSourceMap = MODE === "development";

// ファイル出力時の絶対パス指定に使用
const path = require('path');

// プラグイン
// js最適化
const TerserPlugin = require('terser-webpack-plugin');

const VueLoaderPlugin = require('vue-loader/lib/plugin')


module.exports = {
  // エントリーポイント(メインのjsファイル)
  entry: {
    create_question: './src/create_question.js',
    create_question_group: './src/create_question_group.js',
    edit_question: './src/edit_question.js',
    scan_question: './src/scan_question.js',
    training_question: './src/training_question.js',
    training_answer: './src/training_answer.js',
  },
  // ファイルの出力設定
  output: {
    // 出力先(絶対パスでの指定必須)
    path: path.resolve(__dirname, 'dist'),
    // 出力ファイル名
    filename: '[name].js',
  },
  mode: MODE,
  // ソースマップ有効
  devtool: 'source-map',
  // ローダーの設定
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        // ローダーの対象 // 拡張子 .js の場合
        test: /\.js$/,
        // ローダーの処理対象から外すディレクトリ
        exclude: /node_modules/,
        // Babel を利用する
        loader: "babel-loader",
      },
      {
          test: /\.css$/,
          use: [
              "vue-style-loader",
              "css-loader",
          ],
      },
    ]
  },
  // import 文で .ts ファイルを解決するため
  resolve: {
    // Webpackで利用するときの設定
    extensions: ["*", ".js", ".vue", ".json"]
  },
  plugins: [
    // Vueを読み込めるようにするため
    new VueLoaderPlugin()
  ],
  // mode:puroductionでビルドした場合のファイル圧縮
  optimization: {
    minimizer: enabledSourceMap
      ? [
        // jsファイルの最適化
        new TerserPlugin({
          // すべてのコメント削除
          extractComments: 'all',
          // console.logの出力除去
          terserOptions: {
            compress: { drop_console: true }
          },
        }),
      ] : []
  },
  // js, css, html更新時自動的にブラウザをリロード
  devServer: {
    // サーバーの起点ディレクトリ
    // contentBase: "dist",
    // バンドルされるファイルの監視 // パスがサーバー起点と異なる場合に設定
    publicPath: '/dist/',
    //コンテンツの変更監視をする
    watchContentBase: true,
  }
};