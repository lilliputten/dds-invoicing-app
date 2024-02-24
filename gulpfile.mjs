// --@ts-check

import fs from 'fs';
import path from 'path';

import gulp from 'gulp';
// import gulpRename from 'gulp-rename';
// import gulpPrettify from 'gulp-html-prettify';

import gulpConcat from 'gulp-concat';

import sourcemaps from 'gulp-sourcemaps';
import gulpLess from 'gulp-less';
import gulpAutoprefixer from 'gulp-autoprefixer';

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

const watchOptions = {
  // @see: https://gulpjs.com/docs/en/getting-started/watching-files/
  events: 'all',
  /** Omit initial action for watch cycles */
  ignoreInitial: true,
  delay: 1000,
  // NOTE: There is a bug with styles compiling watching by `livereload-server`: it takes only previous state, needs to make one extra update
};

const stylesSrcAll = ['assets-src/blocks/**/*.less'];
const stylesSrcEntry = 'assets-src/_blocks_less.less';
const stylesDest = staticPath + 'generated/css/';
const lessConfig = {
  paths: [path.join(prjPath, staticPath)],
  sourceMaps: true,
};

/** Use a delay to confirm update of styles for `livereload-server`.
 * Use only if watch task has run.
 */
const finishGenerationDelay = 2000;

let isWatchTask = false;
let finishedStylesHandler = undefined;

function finishedStyles() {
  return new Promise((resolve) => {
    if (finishedStylesHandler) {
      clearTimeout(finishedStylesHandler);
    }
    finishedStylesHandler = setTimeout(
      () => {
        finishedStylesHandler = null;
        const dateStr = formatDate(null, timeZone, timeTagFormat);
        // eslint-disable-next-line no-console
        console.log('finishedStyles:', dateStr);
        fs.writeFile(stylesDest + 'generated.txt', dateStr, resolve);
      },
      // NOTE: Use delay only for watched tasks
      isWatchTask ? finishGenerationDelay : 0,
    );
  });
}

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
      // xxx
      .on('end', finishedStyles)
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
function copyAssetsToStatic() {
  return gulp.src(assetsSrc, { base: './assets-src' }).pipe(gulp.dest(staticPath));
}
gulp.task('copyAssetsToStatic', copyAssetsToStatic);
gulp.task('copyAssetsToStaticWatch', () => {
  isWatchTask = true;
  return gulp.watch(assetsSrc, watchOptions, copyAssetsToStatic);
});

const updateAllTasks = [
  // Watch all tasks...
  'compileStyles',
  'copyAssetsToStatic',
].filter(Boolean);
gulp.task('updateAll', gulp.parallel.apply(gulp, updateAllTasks));

const watchAllTasks = [
  // Watch all tasks...
  'compileStylesWatch',
  'copyAssetsToStaticWatch',
].filter(Boolean);
gulp.task('watchAll', gulp.parallel.apply(gulp, watchAllTasks));
