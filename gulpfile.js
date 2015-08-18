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

gulp.task('replace', ['coffee', 'react'], function() {
  return glob('./chendian/static/js/frontend/**/*.js', function(er, files) {
    files.map(function(srcName) {
      var name = srcName.split('/');
      name = name[name.length - 1];
      var js_name = name.split('-')[0];
      var regex = new RegExp('(js\/frontend\/(?:normal\/)?)' + escapeRegExp(js_name) + '[^\/"\']*\.js', 'ig');

      // 替换模板文件
      glob('./chendian/templates/frontend/**/*.html', function(er, files) {
        files.map(function(htmlpath) {
          var source = fs.readFileSync(htmlpath, encoding='utf-8');
          var dest = htmlpath;
          // 替换 js 文件路径
          var data = source.replace(regex, '$1' + name);
          fs.writeFileSync(dest, data);
        });
      });

    });
  });
});

gulp.task('watch', function() {
  return gulp.watch(
    ['./chendian/static/js/**/*.jsx', './chendian/static/js/**/*.coffee'],
    ['replace']
  );
});

function escapeRegExp(string){
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
