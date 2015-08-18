bookDetailAPI = '/api/books/' + $('#content').data('id') + '/'

# 更新页面上的书籍信息
updatePage = (data) ->
  $("#book_name").text data.name
  $("#book_author").text data.author
  if data.douban_url
    $("#book_douban_url").prop 'href', data.douban_url
  description = filterXSS(data.description)
  description = description.replace /\r\n/g, '<br />'
  description = description.replace /\n/g, '<br />'
  $("#book_description").html description
  $("#book_cover").prop 'src', data.cover

# 发送更新书籍信息的请求
send = (data) ->
  $.ajax
    url: bookDetailAPI,
    method: 'PATCH',
    data: data,
    success: (data) ->
      updatePage data
      alert '更新成功'
      $('#editBookModal').modal 'hide'
    error: (data) ->
      alert 'error'

# 获取表单数据并发送
submitForm = ->
  # 获取表单数据
  data = {}
  $('#editBookForm').serializeArray().map (item) ->
    data[item.name] = item.value

  jsonData = JSON.stringify data

  send jsonData

# 填充 modal 内表单内容
fillForm = (data) ->
  $('#name').val data.name
  $('#author').val data.author
  $('#isbn').val data.isbn
  $('#douban_url').val data.douban_url
  $('#description').val data.description
  $("#cover").val data.cover
  $("#cover_up").prop "src", data.cover

# 点击提交按钮事件
bindSubmitEvent = (selector) ->
  $(selector).on('click', (e) ->
    e.preventDefault()
    submitForm()
    return false
  )

# 显示 modal 时获取 book 信息
$('#editBookModal').on('show.bs.modal', (e) ->
  $.ajax
    url: bookDetailAPI,
    success: (data) ->
      fillForm data
      bindSubmitEvent '#editBookButton'
      try
        initDropzone()
      catch error
        console.warn error
)

# dropzone
initDropzone = ->
  dropzone = new Dropzone "#cover_up",
    paramName: "file",
    url: "/api/upload/"

  dropzone.on "sending", (file, xhr, tformData) ->
    tformData.append "csrfmiddlewaretoken", csrftoken
  dropzone.on "success", (file, resp) ->
    $("#cover").val resp.url
    $("#cover_up").prop "src", resp.url

  $("#cover_up").removeClass "hide"
