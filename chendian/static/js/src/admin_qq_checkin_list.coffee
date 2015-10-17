$ ->
  urlBase = $('meta[name="url-detail"]')[0].content

  # 载入 form
  loadEditForm = (id) ->
    url = urlBase.replace("0", id)
    $("#edit_form").html("loading....")

    $.get url, (record) ->
      template = $("#edit_form_template").html()
      rendered = Mustache.render(template, record)
      $("#edit_form").html(rendered)
      $("#post_edit_form").data("id", id)

  # modal
  $(".edit_record").on "click", ->
    id = $(this).data("id")
    loadEditForm(id)
    $("#edit_modal").modal("show")

  # post form
  $("#post_edit_form").on "click", ->
    id = $(this).data("id")
    jsonData = {}
    $("#edit_form_post").serializeArray().map (item) ->
      if (item.name == 'sn')
        item.value = item.value || null
      jsonData[item.name] = item.value

    jsonData = JSON.stringify(jsonData)
    url = urlBase.replace "0", id
    $.ajax
      type: "PUT",
      url: url,
      data: jsonData,
      dataType: "json",
      contentType : "application/json",
      success: (data) ->
        location.reload()

  # delete
  $(".delete_record").on "click", ->
    if (!confirm("确定要删除?"))
      return false

    id = $(this).data("id")
    url = urlBase.replace "0", id
    $.ajax
      type: "DELETE",
      url: url
      dataType: "json",
      success: (data) ->
        location.reload()
