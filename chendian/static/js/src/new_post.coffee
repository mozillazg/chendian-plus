# 判断是否是数组
typeIsArray = Array.isArray || ( value ) ->
  return {}.toString.call( value ) is '[object Array]'

uploadFile = (file) ->
  data = new FormData()
  imgURL = ''
  data.append 'file', file
  $.ajax
    method: 'POST'
    url: '/api/upload/'
    data: data
    processData: false
    contentType: false
    async: false
    success: (data) ->
      imgURL = data.url
  imgURL

# 给文本框应用 Summernote
initSummernote = (selector) ->
  updateTextarea = ->
    $(selector).val $(selector).code()
    $(selector).change()
  $(selector).summernote
    lang: 'zh-CN'
    height: '150px'
    toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['height', ['height']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'hr']],
        # ['view', ['fullscreen', 'codeview']],
        ['help', ['help']]
    ]
    onKeyup: (e) ->
      updateTextarea()
    onChange: ->
      updateTextarea()
    onImageUpload: (files) ->
      $note = $(@)
      url = uploadFile files[0]
      if url
        $note.summernote('insertImage', url)

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

# 获取分类
fetchCategories = ($select) ->
  options = ajaxOptions('/api/blog/categories/', 'id')
  $select.select2
    ajax: options

# 发送数据
newPost = (data, form) ->
  $.ajax
    url: '/api/blog/articles/'
    method: 'POST'
    data: data
    success: (data) ->
      alert '投稿成功'
      window.location.reload()
    error: (data) ->
      alert '所有表单项均不能为空，请修正错误'

# 显示 Modal 时初始化表单
$('#newPostModal').on('show.bs.modal', (e) ->
  fetchTags($('#tags'))
  fetchCategories($('#categories'))
  initSummernote('#new-post-content')
)

# 点击投递按钮时，发送表单内容
$('#newPostButton').on('click', ->
  data = {}
  $('#newPostForm').serializeArray().map (item) ->
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
