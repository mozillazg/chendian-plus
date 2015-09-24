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
  newString.replace /\n/g, '<br>'

newline2p = (str, option) ->
  if option == undefined
    option =
      includeBr: false
  if option.includeBr
    array = replaceLinesep(str).split /\n{2,}/
  else
    array = replaceLinesep(str).split /\n/
  newArray = for s in array
    newline2br "<p>#{s}</p>"

  newArray.join('')

text2html = (str, option) ->
  html = str.replace /[ ]/g, '&nbsp;'
  newline2p str, option


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
  navsA = $ '.navbar-nav > li  a'
  currentPath = location.pathname
  path_map = {}
  sub_paths = [
    '/admin123/blog/articles/',
    '/admin123/blog/tags/',
    '/admin123/blog/categories/',
    '/admin123/books/',
    '/admin123/books/hot/',
    '/admin123/records/checkins/',
    '/admin123/analysis/group-by-qq/'
  ]

  maxLengthItem = (items) ->
    max = items[0]
    for item in items
      if item.pathname.length > max.pathname.length
        max = item
    max

  # 保存跟当前路径有关的导航栏
  for a in navsA
    if currentPath == a.pathname or (
      currentPath != '/' and currentPath.indexOf(a.pathname) != -1
    )
      if not path_map.hasOwnProperty currentPath
        path_map[currentPath] = []
      path_map[currentPath].push a

  for path, navs of path_map
      max = maxLengthItem navs
      $(navsLi).removeClass 'active'
      if max.pathname != '/'
        $(max).parent().addClass 'active'
        if max.pathname in sub_paths
          $(max).closest('li').parent().closest('li').addClass 'active'
  return


class API
  constructor: (@url) ->

  request: (method, callback, option) ->
    option = option or {}
    $.ajax
      type: method,
      data: option.data or {},
      url: @url,
      dataType: "json",
      success: (data) ->
        callback()

lazyClickHandler = (callback, option) ->
  msg = $(this).data("msg")
  if (!confirm(msg))
    return false

  url = $(this).data("url")
  method = $(this).data("method")
  api = new API url
  _callback = ->
    if callback
      callback.bind(this)()
    else
      location.reload()

  api.request method, ->
     _callback.bind(this)()
    , option


setupEditable = ->
  $.fn.editable.defaults.ajaxOptions = {type: 'patch', dataType: 'json'}
  $.fn.editable.defaults.params = (params) ->
    # originally params contain pk, name and value
    name = params.name
    value = params.value
    delete params['name']
    delete params['value']
    delete params['pk']
    params[name] = value
    return params
  $.fn.editable.defaults.validate = (value) ->
    if $.trim(value) == ''
      return'This field is required'
