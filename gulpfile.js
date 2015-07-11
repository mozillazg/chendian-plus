var coffee = require('gulp-coffee');
var del = require('del');
var fs = require("fs");
var glob = require('glob');
var gulp = require('gulp');
var gutil = require('gulp-util');
var react = require('gulp-react');
var replace = require("gulp-replace");
var rev = require('gulp-rev');

gulp.task('default', ['replace']);

gulp.task('coffee', function() {
  setTimeout(function () {
    gulp.src('./chendian/static/js/src/*.coffee')
    .pipe(coffee({bare: true}).on('error', gutil.log))
    .pipe(rev())
    .pipe(gulp.dest('./chendian/static/js/frontend/'))
  }, 1000);
});

gulp.task('react', function() {
  setTimeout(function () {
    var dest = './chendian/static/js/frontend/';
    del(dest + '*.js');
    gulp.src('chendian/static/js/src/*.jsx')
    .pipe(react())
    .pipe(rev())
    .pipe(gulp.dest(dest));
  }, 1000);
});

gulp.task('replace', ['react', 'coffee'], function() {
  glob('./chendian/static/js/frontend/*.js', function(er, files) {
    files.map(function(srcName) {
      var name = srcName.split('/');
      name = name[name.length - 1];
      var js_name = name.split('-')[0];
      var regex = new RegExp('(frontend/)' + escapeRegExp(js_name) + '[^\.]*\.js(?=">)', 'ig');

      // 替换模板文件
      glob('./chendian/templates/frontend/**/*.html',
            function(er, files) {
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
  gulp.watch(
    ['./chendian/static/js/**/*.jsx', './chendian/static/js/**/*.coffee'],
    ['replace']
  );
});

function escapeRegExp(string){
  string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
