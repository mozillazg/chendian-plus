$(function() {
  var addIndex, loadCheckinList, urlList;
  urlList = $('meta[name="url-list"]')[0].content;
  addIndex = function(arr) {
    var i, results;
    i = 1;
    results = [];
    while (i <= arr.length) {
      arr[i - 1]['n'] = i;
      results.push(i++);
    }
    return results;
  };
  loadCheckinList = function(data) {
    $("#checkin_list").html("loading....");
    return $.get(urlList, data, function(checkin_list) {
      var rendered, template;
      template = $("#checkin_list_template").html();
      addIndex(checkin_list);
      rendered = Mustache.render(template, {
        "data": checkin_list
      });
      return $("#checkin_list").html(rendered);
    });
  };
  return $(".view_check_list").on('click', function() {
    var data;
    data = {
      "sn": $(this).data("sn"),
      "qq": $(this).data("qq"),
      "nick_name": $(this).data("nick_name"),
      "book_name": $(this).data("book_name"),
      "datetime_start": $(this).data("datetime_start"),
      "datetime_end": $(this).data("datetime_end")
    };
    loadCheckinList(data);
    return $("#myModal").modal("show");
  });
});
