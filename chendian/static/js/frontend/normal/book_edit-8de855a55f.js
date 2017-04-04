var bindSubmitEvent, bookDetailAPI, fillForm, initDropzone, sendUpdate, submitForm, updatePage;

bookDetailAPI = '/api/books/' + $('#content').data('id') + '/';

updatePage = function(data) {
  var description;
  $("#book_name").text(data.name);
  $("#book_author").text(data.author);
  $("#book_isbn").text(data.isbn);
  if (data.douban_url) {
    $("#book_douban_url").prop('href', data.douban_url);
  }
  description = filterXSS(data.description);
  description = newline2p(data.description);
  $("#book_description").html(description);
  return $("#book_cover").prop('src', data.cover);
};

sendUpdate = function(data) {
  return $.ajax({
    url: bookDetailAPI,
    method: 'PATCH',
    data: data,
    success: function(data) {
      updatePage(data);
      alert('更新成功');
      return $('#editBookModal').modal('hide');
    },
    error: function(data) {
      return alert('error');
    }
  });
};

submitForm = function() {
  var data, jsonData;
  data = {};
  $('#editBookForm').serializeArray().map(function(item) {
    return data[item.name] = item.value;
  });
  jsonData = JSON.stringify(data);
  return sendUpdate(jsonData);
};

fillForm = function(data) {
  $('#name').val(data.name);
  $('#author').val(data.author);
  $('#isbn').val(data.isbn);
  $('#douban_url').val(data.douban_url);
  $('#description').val(data.description);
  $("#cover").val(data.cover);
  return $("#cover_up").prop("src", data.cover);
};

bindSubmitEvent = function(selector) {
  return $(selector).on('click', function(e) {
    e.preventDefault();
    e.stopPropagation();
    submitForm();
    e.stopImmediatePropagation();
    return false;
  });
};

$('#editBookModal').on('show.bs.modal', function(e) {
  return $.ajax({
    url: bookDetailAPI,
    success: function(data) {
      var error, error1;
      fillForm(data);
      bindSubmitEvent('#editBookButton');
      try {
        return initDropzone();
      } catch (error1) {
        error = error1;
        return console.warn(error);
      }
    }
  });
});

initDropzone = function() {
  var dropzone;
  dropzone = new Dropzone("#cover_up", {
    paramName: "file",
    url: "/api/upload/"
  });
  dropzone.on("sending", function(file, xhr, tformData) {
    tformData.append("csrfmiddlewaretoken", csrftoken);
    return $(".uploading.child").removeClass("hide");
  });
  dropzone.on("success", function(file, resp) {
    $(".uploading.child").addClass("hide");
    $("#cover").val(resp.url);
    return $("#cover_up").prop("src", resp.url);
  });
  return $("#cover_up").removeClass("hide");
};
