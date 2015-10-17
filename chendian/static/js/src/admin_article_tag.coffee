$( ->
  setupEditable()
  $('.editable').editable()

  # delete
  $(".delete_record").on "click", ->
    func = ->
      $(@).closest('tr').remove()
    lazyClickHandler.bind(@) func.bind(@)

  $(".newObj").on "click", ->
    $("#add_modal").modal "show"

  $("#post_add_form").on "click", ->
    jsonData = {}
    $("#add_form_post").serializeArray().map (item) ->
      jsonData[item.name] = item.value

    jsonData = JSON.stringify(jsonData)

    url = $('meta[name="list-url"]')[0].content

    $.ajax
      type: "POST",
      url: url,
      dataType: "json",
      contentType : "application/json",
      data: jsonData,
      success: (data) ->
        location.reload()
)
