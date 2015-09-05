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

# 将换行符统一为 \n
replaceLinesep = (str) ->
  newString = str.replace /\r\n/g, '\n'
  newString.replace /\r/g, '\n'

# newline -> <br />
newline2br = (str) ->
  newString = replaceLinesep str
  newString.replace /\n/g, '<br />'

newline2p = (str) ->
  array = replaceLinesep(str).split /\n{2,}/
  newArray = for s in array
    newline2br "<p>#{s}</p>"

  newArray.join('')

text2html = (str) ->
  html = str.replace /[ ]/g, '&nbsp;'
  html = newline2p str
  newline2br html


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

# 高亮导航栏
heightlightNav = ->
  navsLi = $ '.navbar-nav > li'
  navsA = $ '.navbar-nav > li > a'
  currentPath = location.pathname
  for a in navsA
    if currentPath == a.pathname or (
      currentPath != '/' and currentPath.indexOf(a.pathname) != -1
    )
      $(navsLi).removeClass 'active'
      $(a).parent().addClass 'active'
      break
  return
