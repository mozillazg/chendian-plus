$(function() {
  setupEditable();
  $('.editable').editable();
  $(".delete_record").on("click", function() {
    var func;
    func = function() {
      return $(this).closest('tr').remove();
    };
    return lazyClickHandler.bind(this)(func.bind(this));
  });
  $(".newObj").on("click", function() {
    return $("#add_modal").modal("show");
  });
  return $("#post_add_form").on("click", function() {
    var jsonData, url;
    jsonData = {};
    $("#add_form_post").serializeArray().map(function(item) {
      return jsonData[item.name] = item.value;
    });
    jsonData = JSON.stringify(jsonData);
    url = $('meta[name="list-url"]')[0].content;
    return $.ajax({
      type: "POST",
      url: url,
      dataType: "json",
      contentType: "application/json",
      data: jsonData,
      success: function(data) {
        return location.reload();
      }
    });
  });
});
