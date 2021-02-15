const path=require('path')
const { CleanWebpackPlugin}=require('clean-webpack-plugin');

module.exports={
    entry:{
        "mainpage":"./resources/mainpage.js",
        "index":"./resources/index.js",
    },
    output:{
        "filename":"[name].js",
        "path":path.resolve(__dirname,'static/js')
    },
    module:{
        rules:[
            {
                test:/\.js$/,
                use:[
                    'babel-loader'
                ]
            }
        ]
    },
    plugins:[
        new CleanWebpackPlugin(),
    ]
}