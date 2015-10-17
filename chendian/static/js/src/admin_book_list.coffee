$( ->

  # 载入 form
  loadEditForm = (id, url) ->
    $("#edit_form").html "loading...."
    $.get(url, (record) ->
      template = $("#edit_form_template").html()
      rendered = Mustache.render template, record
      $("#edit_form").html rendered
      $("#post_edit_form").data "id", id
      $("#post_edit_form").data "url", url
    )

  # modal
  $(".edit_record").on "click", ->
    id = $(this).data("id")
    url = $(this).data 'url'
    loadEditForm(id, url)
    $("#edit_modal").modal "show"

  # post form
  $("#post_edit_form").on "click", ->
    id = $(this).data "id"
    jsonData = {}
    $("#edit_form_post").serializeArray().map((item) ->
      jsonData[item.name] = item.value
    )

    jsonData = JSON.stringify(jsonData)
    url = $(this).data "url"
    $.ajax
      type: "PUT",
      url: url,
      data: jsonData,
      dataType: "json",
      contentType : "application/json",
      success: ->
        location.reload()

  # delete
  $(".delete_record").on "click", ->
    if (!confirm("确定要删除?"))
      return false

    url = $(this).data "url"
    $.ajax
      type: "DELETE",
      url: url,
      dataType: "json",
      success: (data) ->
        location.reload()
)
