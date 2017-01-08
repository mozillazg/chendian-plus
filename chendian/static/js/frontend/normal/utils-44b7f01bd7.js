var API, escapeHtml, form2json, heightlightNav, lazyClickHandler, loadingDiv, newline2br, newline2p, replaceLinesep, setupEditable, text2html, typeIsArray, uploadFile,
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

typeIsArray = Array.isArray || function(value) {
  return {}.toString.call(value) === '[object Array]';
};

uploadFile = function(file, callback) {
  var data;
  data = new FormData();
  data.append('file', file);
  return $.ajax({
    method: 'POST',
    url: '/api/upload/',
    data: data,
    processData: false,
    contentType: false,
    success: function(data) {
      return callback(data.url);
    }
  });
};

replaceLinesep = function(str) {
  var newString;
  newString = str.replace(/\r\n/g, '\n');
  return newString.replace(/\r/g, '\n');
};

newline2br = function(str) {
  var newString;
  newString = replaceLinesep(str);
  return newString.replace(/\n/g, '<br>');
};

newline2p = function(str, option) {
  var array, newArray, s;
  if (option === void 0) {
    option = {
      includeBr: false
    };
  }
  if (option.includeBr) {
    array = replaceLinesep(str).split(/\n{2,}/);
  } else {
    array = replaceLinesep(str).split(/\n/);
  }
  newArray = (function() {
    var i, len, results;
    results = [];
    for (i = 0, len = array.length; i < len; i++) {
      s = array[i];
      results.push(newline2br("<p>" + s + "</p>"));
    }
    return results;
  })();
  return newArray.join('');
};

text2html = function(str, option) {
  var html;
  html = str.replace(/[ ]/g, '&nbsp;');
  return newline2p(str, option);
};

form2json = function($form) {
  var data;
  data = {};
  $form.serializeArray().map(function(item) {
    return data[item.name] = item.value;
  });
  return JSON.stringify(data);
};

loadingDiv = function() {
  return '<div class="loading"> <img src="https://dn-tmp.qbox.me/loading/red/loading-bars.svg" /> </div>';
};

escapeHtml = function(str) {
  var div;
  div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
};

heightlightNav = function() {
  var a, currentPath, i, len, max, maxLengthItem, navs, navsA, navsLi, path, path_map, ref, sub_paths;
  navsLi = $('.navbar-nav > li');
  navsA = $('.navbar-nav > li  a');
  currentPath = location.pathname;
  path_map = {};
  sub_paths = ['/admin123/blog/articles/', '/admin123/blog/tags/', '/admin123/blog/categories/', '/admin123/books/', '/admin123/books/hot/', '/admin123/records/checkins/', '/admin123/analysis/group-by-qq/'];
  maxLengthItem = function(items) {
    var i, item, len, max;
    max = items[0];
    for (i = 0, len = items.length; i < len; i++) {
      item = items[i];
      if (item.pathname.length > max.pathname.length) {
        max = item;
      }
    }
    return max;
  };
  for (i = 0, len = navsA.length; i < len; i++) {
    a = navsA[i];
    if (currentPath === a.pathname || (currentPath !== '/' && currentPath.indexOf(a.pathname) !== -1)) {
      if (!path_map.hasOwnProperty(currentPath)) {
        path_map[currentPath] = [];
      }
      path_map[currentPath].push(a);
    }
  }
  for (path in path_map) {
    navs = path_map[path];
    max = maxLengthItem(navs);
    $(navsLi).removeClass('active');
    if (max.pathname !== '/') {
      $(max).parent().addClass('active');
      if (ref = max.pathname, indexOf.call(sub_paths, ref) >= 0) {
        $(max).closest('li').parent().closest('li').addClass('active');
      }
    }
  }
};

API = (function() {
  function API(url1) {
    this.url = url1;
  }

  API.prototype.request = function(method, callback, option) {
    option = option || {};
    return $.ajax({
      type: method,
      data: option.data || {},
      url: this.url,
      dataType: "json",
      success: function(data) {
        return callback();
      }
    });
  };

  return API;

})();

lazyClickHandler = function(callback, option) {
  var _callback, api, method, msg, url;
  msg = $(this).data("msg");
  if (!confirm(msg)) {
    return false;
  }
  url = $(this).data("url");
  method = $(this).data("method");
  api = new API(url);
  _callback = function() {
    if (callback) {
      return callback.bind(this)();
    } else {
      return location.reload();
    }
  };
  return api.request(method, function() {
    return _callback.bind(this)();
  }, option);
};

setupEditable = function() {
  $.fn.editable.defaults.ajaxOptions = {
    type: 'patch',
    dataType: 'json'
  };
  $.fn.editable.defaults.params = function(params) {
    var name, value;
    name = params.name;
    value = params.value;
    delete params['name'];
    delete params['value'];
    delete params['pk'];
    params[name] = value;
    return params;
  };
  return $.fn.editable.defaults.validate = function(value) {
    if ($.trim(value) === '') {
      return 'This field is required';
    }
  };
};
