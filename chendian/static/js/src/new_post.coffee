typeIsArray = Array.isArray || ( value ) ->
  return {}.toString.call( value ) is '[object Array]'

fetchTags = ($select) ->
  $.ajax
    url: "/api/blog/tags/"
    success: (data) ->
      $select.html ""
      data.map (tag) ->
        option = new Option(tag.name, tag.name)
        $select.get(0).options.add option

fetchCategories = ($select) ->
  $.ajax
    url: "/api/blog/categories/"
    success: (data) ->
      $select.html ""
      data.map (category) ->
        option = new Option(category.name, category.id)
        $select.get(0).options.add option

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
