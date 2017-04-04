var csrfSafeMethod, csrftoken, getCookie;

$(document).ready(function() {
  $("#datetime_start").datetimepicker({
    format: "Y-m-d H:i",
    defaultTime: "00:00"
  });
  return $("#datetime_end").datetimepicker({
    format: "Y-m-d H:i",
    defaultTime: "00:00"
  });
});

getCookie = function(name) {
  var cookie, cookieValue, cookies, i, len;
  cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    cookies = document.cookie.split(';');
    for (i = 0, len = cookies.length; i < len; i++) {
      cookie = cookies[i];
      cookie = jQuery.trim(cookie);
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

csrftoken = getCookie('csrftoken');

csrfSafeMethod = function(method) {
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
};

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
      return xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

heightlightNav();
