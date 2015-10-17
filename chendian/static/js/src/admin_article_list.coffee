$( ->
    handler = ->
      lazyClickHandler.bind(this)()

    # delete
    $(".delete_record").on "click", handler

    # approve
    $('.approve_record').on 'click', handler

    # disapprove
    $('.disapprove_record').on 'click', handler
)
