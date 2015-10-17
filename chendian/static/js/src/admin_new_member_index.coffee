$( ->
  urlBase = $('meta[name="url-detail"]')[0].content

  # approve
  $(".approve_record").on "click", ->
    if (!confirm("确定要导入?"))
      return false

    id = $(this).data("id")
    $.ajax
      type: "PUT",
      url: urlBase.replace("0", id),
      dataType: "json",
      success: (data) ->
        location.reload()

  # delete
  $(".delete_record").on "click", ->
    if (!confirm("确定要忽略?"))
      return false

    id = $(this).data("id")
    $.ajax
      type: "DELETE",
      url: urlBase.replace("0", id),
      dataType: "json",
      success: (data) ->
        location.reload()

)
