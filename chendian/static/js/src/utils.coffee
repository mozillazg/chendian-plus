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
newline2br = (str) ->
  newString = str.replace /\r\n/g, '<br />'
  newString.replace /\n/g, '<br />'

newline2p = (str) ->
  array = str.split /\r\n|\n|\r/
  newArray = for s in array
    if s == ''
      '<br>'
    else
      "<p>#{s}</p>"

  newArray.join('').replace /\s/g, '&nbsp;'


form2json = ($form) ->
  # 获取表单数据
  data = {}
  $form.serializeArray().map (item) ->
    data[item.name] = item.value

  JSON.stringify data

loadingDiv = () ->
  '<div class="loading">
    <img src="https://dn-tmp.qbox.me/loading/red/loading-bars.svg" />
  </div>'

escapeHtml = (str) ->
  div = document.createElement 'div'
  div.appendChild document.createTextNode str
  div.innerHTML
