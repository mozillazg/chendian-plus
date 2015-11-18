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
      uploadFile files[0], (url) ->
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
editPost = (data, id) ->
  $.ajax
    url: '/api/blog/articles/' + id
    method: 'put'
    dataType: 'json'
    contentType: 'application/json'
    data: data
    success: (data) ->
      alert '编辑成功'
      $('#editPostModal').modal 'hide'
      location.reload()
    error: (data) ->
      alert '所有表单项均不能为空，请修正错误'

# 填充表单数据
initForm = (id) ->
  $.ajax
    url: '/api/blog/articles/' + id
    async: false
    success: (data) ->
      $('#title').val(data.title)
      $categories = $ '#categories'
      $categories.children().remove()
      $tags = $ '#tags'
      $tags.children().remove()

      for item in data.categories
        html = "<option value='#{item.id}' selected>#{item.name}</option>"
        $option = $ html
        $categories.append $option

      for item in data.tags
        html = "<option value='#{item.id}' selected>#{item.name}</option>"
        $option = $ html
        $tags.append $option

      whiteList = $.extend {}, filterXSS.whiteList
      whiteList.span = ['style']
      content = filterXSS data.content, {whiteList: whiteList}
      $('#edit-post-content').code content

# 显示 Modal 时初始化表单
$('#editPostModal').on('show.bs.modal', (e) ->
  id = $(this).data('id')
  initSummernote('#edit-post-content')
  initForm(id)
  fetchTags($('#tags'))
  fetchCategories($('#categories'))
)

$('.edit_record').on('click', ->
  id = $(this).data('id')
  $modal = $ '#editPostModal'
  $modal.data 'id', id
  $('#editPostButton').data 'id', id

  $modal.modal 'show'
)

# 点击编辑按钮时，发送表单内容
$('#editPostButton').on('click', ->
  id = $(this).data('id')
  data = {}
  $textarea = $('#edit-post-content')
  $textarea.val($textarea.code())

  $('#editPostForm').serializeArray().map (item) ->
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
  editPost jsonData, id
)
