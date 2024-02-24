// --@ts-check

// import fs from 'fs';
import path from 'path';

import gulp from 'gulp';
// import gulpRename from 'gulp-rename';
// import gulpPrettify from 'gulp-html-prettify';

import sourcemaps from 'gulp-sourcemaps';
import gulpLess from 'gulp-less';
import gulpAutoprefixer from 'gulp-autoprefixer';

import browserSyncModule from 'browser-sync';
const browserSync = browserSyncModule.create();
const reload = browserSync.reload;

/* // UNUSED: Attempt to use hot-reload deature
 * // @see: https://jsramblings.com/hot-reloading-gulp-webpack-browsersync/
 * import webpack from 'webpack';
 * import webpackDevMiddleware from 'webpack-dev-middleware';
 * import webpackHotMiddleware from 'webpack-hot-middleware';
 * import browserSyncModule from 'browser-sync';
 * import webpackConfig from './webpack.config.js';
 * const browserSync = browserSyncModule.create();
 * const reload = browserSync.reload;
 * const bundler = webpack(webpackConfig);
 * // @see: https://browsersync.io/docs/options
 * browserSync.init({
 *   server: {
 *     baseDir: './',
 *     middleware: [
 *       webpackDevMiddleware(bundler, {
 *         publicPath: webpackConfig.output.publicPath,
 *         stats: { colors: true },
 *       }),
 *       webpackHotMiddleware(bundler),
 *     ],
 *   },
 * });
 */

/* // UNUSED: For relative paths processing...
 * import replace from 'gulp-replace';
 * import tap from 'gulp-tap';
 */

// const buildPath = 'build/';

import {
  // getBuildInfoText,
  prjPath,
} from './utils/gulp-helpers.js';

const stylesSrcAll = 'static/blocks/**/*.less';
const stylesSrcAssets = 'static/_blocks_less.less';
const stylesDest = 'static/css-generated';
const lessConfig = {
  paths: [path.join(prjPath, 'static')],
  sourceMaps: true,
};
function compileStyles() {
  return gulp
    .src(stylesSrcAssets)
    .pipe(sourcemaps.init())
    .pipe(gulpLess(lessConfig))
    .pipe(gulpAutoprefixer())
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest(stylesDest));
}
gulp.task('compileStyles', compileStyles);
gulp.task('watchCompileStyles', () => {
  // browserSync.init({
  //   server: {
  //     baseDir: './',
  //   },
  // });
  // @see: https://gulpjs.com/docs/en/getting-started/watching-files/
  gulp
    .watch(
      [stylesSrcAll],
      {
        // @see: https://gulpjs.com/docs/en/getting-started/watching-files/
        events: 'all',
        ignoreInitial: true,
      },
      compileStyles,
    )
    .on('change', reload);
});

/* // UNUSED: patchBuildTasks
 * const patchBuildTasks = [
 *   'writeBuildInfo',
 *   'prettifyHtml',
 *   'copyExtraFiles',
 * ].filter(Boolean);
 * gulp.task('patchBuild', gulp.parallel.apply(gulp, patchBuildTasks));
 */
