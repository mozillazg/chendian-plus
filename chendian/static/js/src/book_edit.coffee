
updatePage = (date) ->
  return

send = (data) ->
  $.ajax
    url: '',
    method: 'PATCH',
    data: data,
    success: (data) ->
      updatePage data
    fail: (data) ->
      alert data

submitForm = ->
  return

fillForm = (data) ->
  $('#name').val data.name
  $('#author').val data.author
  $('#isbn').val data.isbn
  $('#duoban_url').val data.douban_url
  $('#description').val data.description

bindSubmitEvent = (selector) ->
  $(selector).on('click', (e) ->
    e.preventDefault()
    submitForm()
  )

$('#editBookModal').on('show.bs.modal', (e) ->
  $.ajax
    url: '/api/books/' + $('#content').data('id') + '/',
    success: (data) ->
      fillForm data
  bindSubmitEvent '#editBookButton'
)
