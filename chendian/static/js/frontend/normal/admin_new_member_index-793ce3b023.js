$(function() {
  var urlBase;
  urlBase = $('meta[name="url-detail"]')[0].content;
  $(".approve_record").on("click", function() {
    var id;
    if (!confirm("确定要导入?")) {
      return false;
    }
    id = $(this).data("id");
    return $.ajax({
      type: "PUT",
      url: urlBase.replace("0", id),
      dataType: "json",
      success: function(data) {
        return location.reload();
      }
    });
  });
  return $(".delete_record").on("click", function() {
    var id;
    if (!confirm("确定要忽略?")) {
      return false;
    }
    id = $(this).data("id");
    return $.ajax({
      type: "DELETE",
      url: urlBase.replace("0", id),
      dataType: "json",
      success: function(data) {
        return location.reload();
      }
    });
  });
});
