$ ->
  textarea = $ 'textarea'
  if textarea.length
    editor = new Simditor
      textarea: 'textarea'
