$ ->
  updateTextarea = ->
    $('#id_content').val $('#id_content').code()
    $('#id_content').change()
  $('#id_content').summernote
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
