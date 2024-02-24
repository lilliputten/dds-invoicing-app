module.exports = {
  presets: [
    [
      '@babel/preset-env',
      {
        // targets: '> 5%, not dead',
        // debug: true,
      },
    ],
    [
      '@babel/preset-typescript',
      {
        // allExtensions: true,
      },
    ],
  ],
  plugins: [['@babel/plugin-proposal-decorators', { legacy: true }]],
};
