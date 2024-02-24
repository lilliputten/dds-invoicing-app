// --@ts-check

import fs from 'fs';
import path from 'path';

import gulp from 'gulp';
// import gulpRename from 'gulp-rename';
// import gulpPrettify from 'gulp-html-prettify';

import gulpConcat from 'gulp-concat';

import sourcemaps from 'gulp-sourcemaps';
import babel from 'gulp-babel';
import gulpLess from 'gulp-less';
import lessPluginGlob from 'less-plugin-glob';
import gulpAutoprefixer from 'gulp-autoprefixer';
// import uglify from 'gulp-uglify-es'; // TODO?

import {
  // getBuildInfoText,
  prjPath,
  formatDate,
  timeTagFormat,
  timeZone,
} from './utils/gulp-helpers.js';

/* // UNUSED: For relative paths processing...
 * import replace from 'gulp-replace';
 * import tap from 'gulp-tap';
 */

const staticPath = 'static/';
const generatedPath = staticPath + '_generated/';

const watchOptions = {
  // @see: https://gulpjs.com/docs/en/getting-started/watching-files/
  events: 'all',
  /** Omit initial action for watch cycles */
  ignoreInitial: true,
  delay: 1000,
  // NOTE: There is a bug with styles compiling watching by `livereload-server`: it takes only previous state, needs to make one extra update
};

// Finish action...
let isWatchTask = false;
let finishedHandler = undefined;
/** Use a delay to confirm update of styles for `livereload-server`.
 * Use only if watch task has run.
 */
const finishGenerationDelay = 2000;
function onFinishDelayed(resolve) {
  finishedHandler = null;
  const dateStr = formatDate(null, timeZone, timeTagFormat);
  // eslint-disable-next-line no-console
  console.log('finished:', dateStr);
  fs.writeFile(generatedPath + 'generated.txt', dateStr, resolve);
}
function onFinish() {
  return new Promise((resolve) => {
    if (finishedHandler) {
      clearTimeout(finishedHandler);
    }
    // NOTE: Use delay only for watched tasks
    const delay = isWatchTask ? finishGenerationDelay : 0;
    const cb = onFinishDelayed.bind(undefined, resolve);
    finishedHandler = setTimeout(cb, delay);
  });
}

// Scripts...
const scriptsSrcAll = ['assets-src/blocks/**/*.js'];
const scriptsDest = generatedPath + 'js/';
function compileScripts() {
  return (
    gulp
      .src(scriptsSrcAll)
      .pipe(sourcemaps.init({ loadMaps: true }))
      .pipe(babel())
      // .pipe(uglify()) // TODO?
      .pipe(gulpConcat('scripts.js'))
      .pipe(sourcemaps.write('.'))
      .pipe(gulp.dest(scriptsDest))
      // Delayed final tasks...
      .on('end', onFinish)
  );
}
gulp.task('compileScripts', compileScripts);
gulp.task('compileScriptsWatch', () => {
  isWatchTask = true;
  return gulp.watch(scriptsSrcAll, watchOptions, compileScripts);
});

// Styles...
const stylesSrcAll = ['assets-src/blocks/**/*.less'];
const stylesSrcEntry = 'assets-src/blocks-index.less';
const stylesDest = generatedPath + 'css/';
const lessConfig = {
  // @see: https://lesscss.org/usage/#less-options
  rootPath: path.join(prjPath, staticPath),
  paths: [path.join(prjPath, staticPath)],
  sourceMaps: true,
  plugins: [lessPluginGlob],
};
function compileStyles() {
  return (
    gulp
      .src(stylesSrcEntry)
      .pipe(sourcemaps.init())
      .pipe(gulpLess(lessConfig))
      .pipe(gulpAutoprefixer())
      .pipe(gulpConcat('styles.css'))
      .pipe(sourcemaps.write('.'))
      .pipe(gulp.dest(stylesDest))
      // Delayed final tasks...
      .on('end', onFinish)
  );
}
gulp.task('compileStyles', compileStyles);
gulp.task('compileStylesWatch', () => {
  isWatchTask = true;
  return gulp.watch(stylesSrcAll, watchOptions, compileStyles);
});

const assetsSrc = [
  // Templates...
  'assets-src/**/*.django',
];
function copyAssets() {
  return gulp.src(assetsSrc, { base: './assets-src' }).pipe(gulp.dest(staticPath));
}
gulp.task('copyAssets', copyAssets);
gulp.task('copyAssetsWatch', () => {
  isWatchTask = true;
  return gulp.watch(assetsSrc, watchOptions, copyAssets);
});

const updateAllTasks = [
  // Watch all tasks...
  'compileStyles',
  'copyAssets',
].filter(Boolean);
gulp.task('updateAll', gulp.parallel.apply(gulp, updateAllTasks));

const watchAllTasks = [
  // Watch all tasks...
  'compileStylesWatch',
  'compileScriptsWatch',
  'copyAssetsWatch',
].filter(Boolean);
gulp.task('watchAll', gulp.parallel.apply(gulp, watchAllTasks));