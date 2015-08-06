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
    data: data
    processData: false
    contentType: false
    success: (data) ->
      url = data.url
  url
