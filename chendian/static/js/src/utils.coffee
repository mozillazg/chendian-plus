# 判断是否是数组
typeIsArray = Array.isArray || ( value ) ->
  return {}.toString.call( value ) is '[object Array]'

# 上传文件
uploadFile = (file, callback) ->
  data = new FormData()
  data.append 'file', file
  $.ajax
    method: 'POST'
    url: '/api/upload/'
    data: data
    processData: false
    contentType: false
    success: (data) ->
      callback data.url

# newline -> <br />
newline2br = (string) ->
  newString = string.replace /\r\n/g, '<br />'
  newString.replace /\n/g, '<br />'

form2json = ($form) ->
  # 获取表单数据
  data = {}
  $form.serializeArray().map (item) ->
    data[item.name] = item.value

  JSON.stringify data
