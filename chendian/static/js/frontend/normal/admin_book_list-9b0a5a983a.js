$(function() {
  var ajaxOptions, fetchTags, loadEditForm;
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
  loadEditForm = function(id, url) {
    $("#edit_form").html("loading....");
    return $.get(url, function(record) {
      var rendered, template;
      template = $("#edit_form_template").html();
      rendered = Mustache.render(template, record);
      $("#edit_form").html(rendered);
      $("#post_edit_form").data("id", id);
      $("#post_edit_form").data("url", url);
      return fetchTags($('#tags'));
    });
  };
  $(".edit_record").on("click", function() {
    var id, url;
    id = $(this).data("id");
    url = $(this).data('url');
    loadEditForm(id, url);
    return $("#edit_modal").modal("show");
  });
  $("#post_edit_form").on("click", function() {
    var id, jsonData, url;
    id = $(this).data("id");
    jsonData = {};
    $("#edit_form_post").serializeArray().map(function(item) {
      var key, v, value;
      key = item.name;
      value = item.value;
      if (key in jsonData) {
        v = jsonData[key];
        if (typeIsArray(v)) {
          return jsonData[key].push(value);
        } else {
          return jsonData[key] = [v, value];
        }
      } else {
        if (key === 'tag_list' || key === 'category_list') {
          return jsonData[key] = [value];
        } else {
          return jsonData[key] = value;
        }
      }
    });
    jsonData = JSON.stringify(jsonData);
    url = $(this).data("url");
    return $.ajax({
      type: "PUT",
      url: url,
      data: jsonData,
      dataType: "json",
      contentType: "application/json",
      success: function() {
        return location.reload();
      }
    });
  });
  return $(".delete_record").on("click", function() {
    var url;
    if (!confirm("确定要删除?")) {
      return false;
    }
    url = $(this).data("url");
    return $.ajax({
      type: "DELETE",
      url: url,
      dataType: "json",
      success: function(data) {
        return location.reload();
      }
    });
  });
});
