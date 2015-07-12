typeIsArray = Array.isArray || ( value ) ->
  return {}.toString.call( value ) is '[object Array]'

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

fetchTags = ($select) ->
  options = ajaxOptions("/api/blog/tags/", "name")
  $select.select2
    ajax: options
    tag: true
    tokenSeparators: [' ']
    initSelection: (element, callback) ->
      data = []

      splitVal = (string, separator) ->
        val = []
        if (string == null || string.length < 1)
          return []
        val = string.split separator
        val = ($.trim(i) for i in val)
        val

      $(splitVal(element.val(), " ")).each ->
        data.push
          id: this,
          text: this

      callback data

fetchCategories = ($select) ->
  options = ajaxOptions("/api/blog/categories/", "id")
  $select.select2
    ajax: options

newPost = (data) ->
  $.ajax
    url: "/api/blog/articles/"
    method: "POST"
    data: data
    success: (data) ->
      alert '投稿成功'
    error: (data) ->
      alert '请修正错误'

$("#newPostModal").on('show.bs.modal', (e) ->
  fetchTags($("#tags"))
  fetchCategories($("#categories"))
)

$("#newPostButton").on('click', ->
  data = {}
  $("#newPostForm").serializeArray().map (item) ->
    key = item.name
    value = item.value
    if key of data
      v = data[key]
      if typeIsArray v
        data[key].push value
      else
        data[key] = [v, value]
    else
      if key in ['tag_list', 'category_list']
        data[key] = [value]
      else
        data[key] = value

  jsonData = JSON.stringify data
  newPost jsonData
)
