$(document).ready ->
  $("#datetime_start").datetimepicker
    format: "Y-m-d H:i",
    defaultTime: "00:00"

  $("#datetime_end").datetimepicker
    format: "Y-m-d H:i",
    defaultTime: "00:00"

getCookie = (name) ->
    cookieValue = null
    if (document.cookie && document.cookie != '')
        cookies = document.cookie.split(';')
        for cookie in cookies
            cookie = jQuery.trim(cookie)
            if (cookie.substring(0, name.length + 1) == (name + '='))
                cookieValue = decodeURIComponent(
                  cookie.substring(name.length + 1)
                )
                break
    return cookieValue

csrftoken = getCookie 'csrftoken'
csrfSafeMethod = (method) ->
    # these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method))

$.ajaxSetup
    # dateType: 'json',
    # contentType: 'application/json',
    beforeSend: (xhr, settings) ->
        if (!csrfSafeMethod(settings.type) && !this.crossDomain)
            xhr.setRequestHeader("X-CSRFToken", csrftoken)

heightlightNav()
