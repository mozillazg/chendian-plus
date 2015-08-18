# 判断是否是数组
typeIsArray = Array.isArray || ( value ) ->
  return {}.toString.call( value ) is '[object Array]'

# 上传文件
uploadFile = (file) ->
  data = new FormData()
  url = ''
  data.append 'file', file
  $.ajax
    method: 'POST'
    url: '/api/upload/'
    async: false
    data: data
    processData: false
    contentType: false
    success: (data) ->
      url = data.url
  url

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
