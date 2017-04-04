$(function() {
  var handler;
  handler = function() {
    return lazyClickHandler.bind(this)();
  };
  $(".delete_record").on("click", handler);
  $('.approve_record').on('click', handler);
  return $('.disapprove_record').on('click', handler);
});
