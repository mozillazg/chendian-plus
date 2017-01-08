var ajaxOptions, fetchCategories, fetchTags, initSummernote, newPost;

initSummernote = function(selector) {
  var updateTextarea;
  updateTextarea = function() {
    $(selector).val($(selector).code());
    return $(selector).change();
  };
  return $(selector).summernote({
    lang: 'zh-CN',
    height: '150px',
    toolbar: [['style', ['style']], ['font', ['bold', 'italic', 'underline', 'clear']], ['fontname', ['fontname']], ['fontsize', ['fontsize']], ['color', ['color']], ['para', ['ul', 'ol', 'paragraph']], ['height', ['height']], ['table', ['table']], ['insert', ['link', 'picture', 'hr']], ['help', ['help']]],
    onKeyup: function(e) {
      return updateTextarea();
    },
    onChange: function() {
      return updateTextarea();
    },
    onImageUpload: function(files) {
      var $note;
      $note = $(this);
      return uploadFile(files[0], function(url) {
        if (url) {
          return $note.summernote('insertImage', url);
        }
      });
    }
  });
};

ajaxOptions = function(url, id) {
  return {
    url: url,
    dataType: 'json',
    delay: 250,
    data: function(params) {
      return {
        search: params.term,
        page: params.page
      };
    },
    processResults: function(data, page) {
      var i, item, items, len;
      items = [];
      for (i = 0, len = data.length; i < len; i++) {
        item = data[i];
        items.push({
          id: item[id],
          text: item.name
        });
      }
      return {
        results: items
      };
    },
    cache: true,
    escapeMarkup: function(markup) {
      return markup;
    },
    minimumInputLength: 2,
    templateResult: function(item) {
      if (!item.name) {
        return 'Loading...';
      }
      return item.name;
    },
    templateSelection: function(item) {
      return item.name;
    }
  };
};

fetchTags = function($select) {
  var options;
  options = ajaxOptions('/api/blog/tags/', 'name');
  return $select.select2({
    ajax: options,
    tag: true,
    tokenSeparators: [',', ';', '，', '；']
  });
};

fetchCategories = function($select) {
  var options;
  options = ajaxOptions('/api/blog/categories/', 'id');
  return $select.select2({
    ajax: options
  });
};

newPost = function(data, form) {
  return $.ajax({
    url: '/api/blog/articles/',
    method: 'POST',
    data: data,
    success: function(data) {
      alert('投稿成功, 请等待管理员审核');
      return $('#newPostModal').modal('hide');
    },
    error: function(data) {
      return alert('所有表单项均不能为空，请修正错误');
    }
  });
};

$('#newPostModal').on('show.bs.modal', function(e) {
  fetchTags($('#tags'));
  fetchCategories($('#categories'));
  return initSummernote('#new-post-content');
});

$('#newPostButton').on('click', function() {
  var data, jsonData;
  data = {};
  $('#newPostForm').serializeArray().map(function(item) {
    var key, v, value;
    key = item.name;
    value = item.value;
    if (key in data) {
      v = data[key];
      if (typeIsArray(v)) {
        return data[key].push(value);
      } else {
        return data[key] = [v, value];
      }
    } else {
      if (key === 'tag_list' || key === 'category_list') {
        return data[key] = [value];
      } else {
        return data[key] = value;
      }
    }
  });
  jsonData = JSON.stringify(data);
  return newPost(jsonData);
});
