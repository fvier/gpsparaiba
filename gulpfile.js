// Setup
import { src, dest, parallel, series, task, watch } from 'gulp';
import pjson from './package.json' with { type: 'json' };

// Plugins
import autoprefixer from 'autoprefixer';
import browserSyncLib from 'browser-sync';
import tildeImporter from 'node-sass-tilde-importer';
import cssnano from 'cssnano';
import pixrem from 'pixrem';
import plumber from 'gulp-plumber';
import postcss from 'gulp-postcss';
import rename from 'gulp-rename';
import gulpSass from 'gulp-sass';
import * as dartSass from 'sass';
import gulUglifyES from 'gulp-uglify-es';
import npmdist from 'gulp-npm-dist';
import rtlcss from 'gulp-rtlcss';
import sourcemaps from 'gulp-sourcemaps';
import concat from 'gulp-concat'; // Added missing import for concat

const browserSync = browserSyncLib.create();
const reload = browserSync.reload;
const sass = gulpSass(dartSass);
const uglify = gulUglifyES.default;

// Relative paths function
function pathsConfig() {
  const appName = `./${pjson.name}`;
  const vendorsRoot = 'node_modules';

  return {
    vendorsJs: [
      './node_modules/bootstrap/dist/js/bootstrap.bundle.js',
      './node_modules/simplebar/dist/simplebar.min.js',
      './node_modules/gumshoejs/dist/gumshoe.polyfills.js',
      './node_modules/apexcharts/dist/apexcharts.min.js',
      './node_modules/prismjs/prism.js',
      './node_modules/prismjs/plugins/normalize-whitespace/prism-normalize-whitespace.js',
      './node_modules/toastify-js/src/toastify.js',
      './node_modules/dragula/dist/dragula.js',
      './node_modules/vanilla-wizard/dist/js/wizard.min.js',
      './node_modules/clipboard/dist/clipboard.min.js',
      './node_modules/moment/moment.js',
      './node_modules/dropzone/dist/min/dropzone.min.js',
      './node_modules/flatpickr/dist/flatpickr.js',
      './node_modules/swiper/swiper-bundle.min.js',
      './node_modules/rater-js/index.js',
      './node_modules/sweetalert2/dist/sweetalert2.min.js',
      './node_modules/inputmask/dist/inputmask.min.js',
      './node_modules/choices.js/public/assets/scripts/choices.min.js',
      './node_modules/nouislider/dist/nouislider.min.js',
      './node_modules/multi.js/dist/multi.min.js',
      './node_modules/quill/dist/quill.min.js',
      './node_modules/wnumb/wNumb.min.js',
      './node_modules/iconify-icon/dist/iconify-icon.min.js',
    ],
    vendorsCSS: [
      './node_modules/dropzone/dist/min/dropzone.min.css',
      './node_modules/flatpickr/dist/flatpickr.css',
      './node_modules/swiper/swiper-bundle.min.css',
      './node_modules/sweetalert2/dist/sweetalert2.min.css',
      './node_modules/choices.js/public/assets/styles/choices.min.css',
      './node_modules/nouislider/dist/nouislider.min.css',
      './node_modules/multi.js/dist/multi.min.css',
      './node_modules/quill/dist/quill.core.css',
      './node_modules/quill/dist/quill.bubble.css',
      './node_modules/quill/dist/quill.snow.css',
    ],
    app: appName,
    templates: `${appName}/templates`,
    css: `${appName}/static/css`,
    scss: `${appName}/static/scss`,
    fonts: `${appName}/static/fonts`,
    images: `${appName}/static/images`,
    js: `${appName}/static/js`,
    vendor: `${appName}/static/vendor`,
  }; // Added closing brace
} // Added closing brace for pathsConfig

const paths = pathsConfig();

// Tasks
const processCss = [
  autoprefixer(), // adds vendor prefixes
  pixrem(), // add fallbacks for rem units
];

const minifyCss = [
  cssnano({ preset: 'default' }), // minify result
];

// Styles autoprefixing and minification
function styles() {
  return src([`${paths.scss}/**/*.scss`])
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        importer: tildeImporter,
        includePaths: [paths.scss],
      }).on('error', sass.logError)
    )
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(sourcemaps.write('.')) // generates .map
    .pipe(dest(paths.css));
}

// Styles autoprefixing and minification for RTL
function rtlstyles() {
  return src([`${paths.scss}/app.scss`])
    .pipe(sourcemaps.init())
    .pipe(
      sass({
        importer: tildeImporter,
        includePaths: [paths.scss],
      }).on('error', sass.logError)
    )
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rtlcss()) // Convert to RTL
    .pipe(rename({ suffix: '-rtl' }))
    .pipe(postcss(minifyCss))
    .pipe(rename({ suffix: '.min', extname: '.css' }))
    .pipe(sourcemaps.write('.')) // generates .map
    .pipe(dest(paths.css));
}

// Vendor CSS minification
function vendorStyles() {
  return src(paths.vendorsCSS, { sourcemaps: true })
    .pipe(concat('vendors.css'))
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css));
}

// Javascript minification
function scripts() {
  return src([`${paths.js}/**/*.js`])
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js));
}

// Vendor Javascript minification
function vendorScripts() {
  return src(paths.vendorsJs, { sourcemaps: true })
    .pipe(sourcemaps.init())
    .pipe(concat('vendors.js'))
    .pipe(dest(paths.js))
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js, { sourcemaps: '.' }));
}

// Whole Plugins
const plugins = function () {
  return src(npmdist(), { base: './node_modules' })
    .pipe(
      rename(function (path) {
        path.dirname = path.dirname.replace(/\/dist/, '').replace(/\\dist/, '');
      })
    )
    .pipe(dest(paths.vendor));
};

// Watch
function watchPaths() {
  watch(`${paths.scss}/**/*.scss`, styles, rtlstyles);
}

// Generate all assets
const build = parallel(styles, plugins, rtlstyles, vendorStyles, scripts, vendorScripts);

// Set up dev environment
const dev = parallel(watchPaths);

task('default', series(build, dev));
task('build', build);
task('dev', dev);