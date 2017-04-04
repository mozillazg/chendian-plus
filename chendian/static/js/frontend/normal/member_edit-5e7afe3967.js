var bindSubmitEvent, fillForm, initDropzone, memberDetailAPI, send, submitForm, updatePage;

memberDetailAPI = '/api/members/' + $('#profile').data('id') + '/';

updatePage = function(data) {
  var description;
  $("#member-nick-name").text(data.nick_name);
  description = filterXSS(data.description);
  description = newline2p(description);
  $("#member-description").html(description);
  return $("#member-avatar").prop('src', data.avatar);
};

send = function(data) {
  return $.ajax({
    url: memberDetailAPI,
    method: 'PATCH',
    data: data,
    success: function(data) {
      updatePage(data);
      alert('更新成功');
      return $('#editMemberModal').modal('hide');
    },
    error: function(data) {
      return alert('error');
    }
  });
};

submitForm = function() {
  var jsonData;
  jsonData = form2json($('#editMemberForm'));
  return send(jsonData);
};

fillForm = function(data) {
  $('#nick_name').val(data.nick_name);
  $('#description').val(data.description);
  $("#avatar").val(data.avatar);
  return $("#avatar_up").prop("src", data.avatar);
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

$('#editMemberModal').on('show.bs.modal', function(e) {
  return $.ajax({
    url: memberDetailAPI,
    success: function(data) {
      var error, error1;
      fillForm(data);
      bindSubmitEvent('#editMemberButton');
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
  dropzone = new Dropzone("#avatar_up", {
    paramName: "file",
    url: "/api/upload/"
  });
  dropzone.on("sending", function(file, xhr, tformData) {
    tformData.append("csrfmiddlewaretoken", csrftoken);
    return $(".uploading.child").removeClass("hide");
  });
  dropzone.on("success", function(file, resp) {
    $(".uploading.child").addClass("hide");
    $("#avatar").val(resp.url);
    return $("#avatar_up").prop("src", resp.url);
  });
  return $("#avatar_up").removeClass("hide");
};
