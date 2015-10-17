$ ->
  urlList = $('meta[name="url-list"]')[0].content

  addIndex = (arr) ->
    i = 1
    while i <= arr.length
      arr[i-1]['n'] = i
      i++

  # 载入详细的打卡情况
  loadCheckinList = (data) ->
    $("#checkin_list").html("loading....")

    $.get urlList, data, (checkin_list) ->
      template = $("#checkin_list_template").html()
      addIndex(checkin_list)
      rendered = Mustache.render(template, {"data": checkin_list})
      $("#checkin_list").html(rendered)

  # modal
  $(".view_check_list").on 'click', ->
    data =
      "sn": $(this).data("sn"),
      "qq": $(this).data("qq"),
      "nick_name": $(this).data("nick_name"),
      "book_name": $(this).data("book_name"),
      "datetime_start": $(this).data("datetime_start"),
      "datetime_end": $(this).data("datetime_end")

    loadCheckinList(data)
    $("#myModal").modal("show")
