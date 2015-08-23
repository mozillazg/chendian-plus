var coffee = require('gulp-coffee');
var del = require('del');
var fs = require("fs");
var glob = require('glob');
var gulp = require('gulp');
var gutil = require('gulp-util');
var react = require('gulp-react');
var replace = require("gulp-replace");
var rev = require('gulp-rev');

gulp.task('default', ['watch']);

gulp.task('css', function() {
  var dest = './chendian/static/css/frontend/';
  del(dest + '*.css');
  return gulp.src('./chendian/static/css/src/*.css')
    .pipe(rev())
    .pipe(gulp.dest(dest))
});

gulp.task('coffee', function() {
  var dest = './chendian/static/js/frontend/normal/';
  del(dest + '*.js');
  return gulp.src('./chendian/static/js/src/*.coffee')
    .pipe(coffee({bare: true}).on('error', gutil.log))
    .pipe(rev())
    .pipe(gulp.dest(dest))
});

gulp.task('react', function() {
  var dest = './chendian/static/js/frontend/';
  del(dest + '*.js');
  return gulp.src('chendian/static/js/src/*.jsx')
    .pipe(react())
    .pipe(rev())
    .pipe(gulp.dest(dest));
});

gulp.task('replace', ['css', 'coffee', 'react'], function() {
  var regexpFrontendJS = function (jsName){
    return new RegExp('(css\/frontend\/)' + escapeRegExp(jsName) + '[^\/"\']*\.js', 'ig');
  }
  replaceStaticFiles(
    './chendian/static/js/frontend/**/*.js',
    regexpFrontendJS,
    './chendian/templates/frontend/**/*.html'
  )

  var regexpFrontendCSS = function (cssName){
    return new RegExp('(css\/frontend\/)' + escapeRegExp(cssName) + '[^\/"\']*\.css', 'ig');
  }
  replaceStaticFiles(
    './chendian/static/css/frontend/**/*.css',
    regexpFrontendCSS,
    './chendian/templates/frontend/**/*.html'
  )

});

gulp.task('watch', function() {
  return gulp.watch(
    ['./chendian/static/js/**/*.jsx', './chendian/static/js/**/*.coffee',
     './chendian/static/css/src/*.css'],
    ['replace']
  );
});

function escapeRegExp(string){
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function replaceStaticFiles(src, regexp, dst) {
  return glob(src, function(er, files) {
    files.map(function(srcName) {
      var name = srcName.split('/');
      name = name[name.length - 1];
      var jsName = name.split('-')[0];
      var regex = regexp;

      // 替换模板文件
      glob(dst, function(er, files) {
        files.map(function(htmlpath) {
          var source = fs.readFileSync(htmlpath, encoding='utf-8');
          var dest = htmlpath;
          var regex = regexp(jsName);
          // 替换 js 文件路径
          var data = source.replace(regex, '$1' + name);
          fs.writeFileSync(dest, data);
        });
      });

    });
  });
};
