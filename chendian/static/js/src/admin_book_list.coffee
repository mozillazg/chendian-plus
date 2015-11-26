$( ->

  # select2 ajax 基本选项
  ajaxOptions = (url, id) ->
    url: url
    dataType: 'json'
    delay: 250
    data: (params) ->
      search: params.term,
      page: params.page
    processResults: (data, page) ->
      items = []
      for item in data
        items.push {
          id: item[id]
          text: item.name
        }
      return results: items
    cache: true
    escapeMarkup: (markup) ->
      markup
    minimumInputLength: 2,
    templateResult: (item) ->
      if !item.name
        return 'Loading...'
      item.name
    templateSelection: (item) ->
      item.name

  # 获取标签
  fetchTags = ($select) ->
    options = ajaxOptions('/api/blog/tags/', 'name')
    $select.select2
      ajax: options
      tag: true
      tokenSeparators: [',', ';', '，', '；']

  # 载入 form
  loadEditForm = (id, url) ->
    $("#edit_form").html "loading...."
    $.get(url, (record) ->
      template = $("#edit_form_template").html()
      rendered = Mustache.render template, record
      $("#edit_form").html rendered
      $("#post_edit_form").data "id", id
      $("#post_edit_form").data "url", url
      fetchTags($('#tags'))
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
      key = item.name
      value = item.value
      if key of jsonData
        v = jsonData[key]
        if typeIsArray v
          jsonData[key].push value
        else
          jsonData[key] = [v, value]
      else
        if key in ['tag_list', 'category_list']
          jsonData[key] = [value]
        else
          jsonData[key] = value
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
