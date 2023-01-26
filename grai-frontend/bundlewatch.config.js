const bundlewatchConfig = {
  files: [
    {
      path: "build/**/*.js",
      maxSize: "500kB",
    },
  ],
}

module.exports = bundlewatchConfig
