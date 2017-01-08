var ajaxOptions, editPost, fetchCategories, fetchTags, initForm, initSummernote;

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

editPost = function(data, id) {
  return $.ajax({
    url: '/api/blog/articles/' + id,
    method: 'put',
    dataType: 'json',
    contentType: 'application/json',
    data: data,
    success: function(data) {
      alert('编辑成功');
      $('#editPostModal').modal('hide');
      return location.reload();
    },
    error: function(data) {
      return alert('所有表单项均不能为空，请修正错误');
    }
  });
};

initForm = function(id) {
  return $.ajax({
    url: '/api/blog/articles/' + id,
    async: false,
    success: function(data) {
      var $categories, $option, $tags, content, html, i, item, j, len, len1, ref, ref1, whiteList;
      $('#title').val(data.title);
      $categories = $('#categories');
      $categories.children().remove();
      $tags = $('#tags');
      $tags.children().remove();
      ref = data.categories;
      for (i = 0, len = ref.length; i < len; i++) {
        item = ref[i];
        html = "<option value='" + item.id + "' selected>" + item.name + "</option>";
        $option = $(html);
        $categories.append($option);
      }
      ref1 = data.tags;
      for (j = 0, len1 = ref1.length; j < len1; j++) {
        item = ref1[j];
        html = "<option value='" + item.name + "' selected>" + item.name + "</option>";
        $option = $(html);
        $tags.append($option);
      }
      whiteList = $.extend({}, filterXSS.whiteList);
      whiteList.span = ['style'];
      content = filterXSS(data.content, {
        whiteList: whiteList
      });
      return $('#edit-post-content').code(content);
    }
  });
};

$('#editPostModal').on('show.bs.modal', function(e) {
  var id;
  id = $(this).data('id');
  initSummernote('#edit-post-content');
  initForm(id);
  fetchTags($('#tags'));
  return fetchCategories($('#categories'));
});

$('.edit_record').on('click', function() {
  var $modal, id;
  id = $(this).data('id');
  $modal = $('#editPostModal');
  $modal.data('id', id);
  $('#editPostButton').data('id', id);
  return $modal.modal('show');
});

$('#editPostButton').on('click', function() {
  var $textarea, data, id, jsonData;
  id = $(this).data('id');
  data = {};
  $textarea = $('#edit-post-content');
  $textarea.val($textarea.code());
  $('#editPostForm').serializeArray().map(function(item) {
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
  return editPost(jsonData, id);
});
