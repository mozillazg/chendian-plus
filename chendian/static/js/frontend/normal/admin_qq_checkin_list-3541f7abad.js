$(function() {
  var loadEditForm, urlBase;
  urlBase = $('meta[name="url-detail"]')[0].content;
  loadEditForm = function(id) {
    var url;
    url = urlBase.replace("0", id);
    $("#edit_form").html("loading....");
    return $.get(url, function(record) {
      var rendered, template;
      template = $("#edit_form_template").html();
      rendered = Mustache.render(template, record);
      $("#edit_form").html(rendered);
      return $("#post_edit_form").data("id", id);
    });
  };
  $(".edit_record").on("click", function() {
    var id;
    id = $(this).data("id");
    loadEditForm(id);
    return $("#edit_modal").modal("show");
  });
  $("#post_edit_form").on("click", function() {
    var id, jsonData, url;
    id = $(this).data("id");
    jsonData = {};
    $("#edit_form_post").serializeArray().map(function(item) {
      if (item.name === 'sn') {
        item.value = item.value || null;
      }
      return jsonData[item.name] = item.value;
    });
    jsonData = JSON.stringify(jsonData);
    url = urlBase.replace("0", id);
    return $.ajax({
      type: "PUT",
      url: url,
      data: jsonData,
      dataType: "json",
      contentType: "application/json",
      success: function(data) {
        return location.reload();
      }
    });
  });
  return $(".delete_record").on("click", function() {
    var id, url;
    if (!confirm("确定要删除?")) {
      return false;
    }
    id = $(this).data("id");
    url = urlBase.replace("0", id);
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
