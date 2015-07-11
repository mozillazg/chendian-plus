var coffee = require('gulp-coffee');
var del = require('del');
var fs = require("fs");
var glob = require('glob');
var gulp = require('gulp');
var gutil = require('gulp-util');
var react = require('gulp-react');
var replace = require("gulp-replace");
var rev = require('gulp-rev');
var revReplace = require("gulp-rev-replace");

gulp.task('default', ['replace']);

gulp.task('coffee', function() {
  var dest = './chendian/static/js/frontend/';
  var manifest = "rev-manifest.json";
  gulp.src('./chendian/static/js/src/*.coffee')
    .pipe(coffee({bare: true}).on('error', gutil.log))
    .pipe(rev())
    .pipe(gulp.dest(dest))
    .pipe(rev.manifest({path: manifest, merge: true}))
    .pipe(gulp.dest(dest));
});

gulp.task('react', function() {
  var dest = './chendian/static/js/frontend/';
  var manifest = "rev-manifest.json";
  gulp.src('chendian/static/js/src/*.jsx')
    .pipe(react())
    .pipe(rev())
    .pipe(gulp.dest(dest))
    .pipe(rev.manifest({path: manifest, merge: true}))
    .pipe(gulp.dest(dest));
});

gulp.task('replace', ['react', 'coffee'], function() {
  var src = './chendian/static/js/frontend/';
  var manifest = gulp.src(src + "rev-manifest.json");
  var dest = './chendian/templates/frontend/'

  return gulp.src("./chendian/templates/frontend/**/*.html")
    .pipe(revReplace({manifest: manifest}))
    .pipe(gulp.dest(dest));
});

gulp.task('watch', function() {
  gulp.watch(
    ['./chendian/static/js/**/*.jsx', './chendian/static/js/**/*.coffee'],
    ['replace']
  );
});
