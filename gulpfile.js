var gulp = require('gulp');
var react = require('gulp-react');
var del = require('del');
var rev = require('gulp-rev');
var glob = require('glob');
var replace = require("gulp-replace");
var fs = require("fs");

gulp.task('default', ['watch']);

gulp.task('react', function() {
  var dest = 'chendian/static/js/frontend/';
  del(dest + '*.js');
  return gulp.src('chendian/static/js/src/*.jsx')
          .pipe(react())
          .pipe(rev())
          .pipe(gulp.dest(dest));
});

gulp.task('replace', ['react'], function() {
  return glob('chendian/static/js/frontend/*.js', function(er, files) {
    files.map(function(srcName) {
      var name = srcName.split('/');
      name = name[name.length - 1];
      var js_name = name.split('-')[0];
      var regex = new RegExp('(frontend/)' + escapeRegExp(js_name) + '[^\.]*\.js(?=">)', 'ig');
      // console.log('src name:   ', srcName);
      // console.log('final name: ', name);
      // console.log('js name:    ', js_name);
      // console.log('regex:      ', regex);

      // 替换模板文件
      glob('chendian/templates/frontend/**/*.html', function(er, files) {
        // console.log('files:      ', files);
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
    ['chendian/static/js/src/*.jsx'],
    ['replace']
  );
});

function escapeRegExp(string){
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
