memberDetailAPI = '/api/members/' + $('#profile').data('id') + '/'

# 更新页面上的成员信息
updatePage = (data) ->
  $("#member-nick-name").text data.nick_name
  description = filterXSS(data.description)
  description = newline2br description
  $("#member-description").html description
  $("#member-avatar").prop 'src', data.avatar

# 发送更新成员信息的请求
send = (data) ->
  $.ajax
    url: memberDetailAPI,
    method: 'PATCH',
    data: data,
    success: (data) ->
      updatePage data
      alert '更新成功'
      $('#editMemberModal').modal 'hide'
    error: (data) ->
      alert 'error'

# 获取表单数据并发送
submitForm = ->
  # 获取表单数据
  jsonData = form2json $('#editMemberForm')
  send jsonData

# 填充 modal 内表单内容
fillForm = (data) ->
  $('#nick_name').val data.nick_name
  $('#description').val data.description
  $("#avatar").val data.avatar
  $("#avatar_up").prop "src", data.avatar

# 点击提交按钮事件
bindSubmitEvent = (selector) ->
  $(selector).on('click', (e) ->
    e.preventDefault()
    submitForm()
    return false
  )

# 显示 modal 时获取 member 信息
$('#editMemberModal').on('show.bs.modal', (e) ->
  $.ajax
    url: memberDetailAPI,
    success: (data) ->
      fillForm data
      bindSubmitEvent '#editMemberButton'
      initDropzone()
)

# dropzone
initDropzone = ->
  dropzone = new Dropzone "#avatar_up",
    paramName: "file",
    url: "/api/upload/"

  dropzone.on "sending", (file, xhr, tformData) ->
    tformData.append "csrfmiddlewaretoken", csrftoken
  dropzone.on "success", (file, resp) ->
    $("#avatar").val resp.url
    $("#avatar_up").prop "src", resp.url

  $("#avatar_up").removeClass "hide"
