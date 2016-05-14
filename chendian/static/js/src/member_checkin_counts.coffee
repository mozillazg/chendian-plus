updateCheckinCounts = (year) ->
  if (isMobile.any)
    return

  domId = "#checkin-count"
  id = $(domId).data "id"
  year = year ? year : (new Date()).getFullYear()

  url = "/api/members/#{id}/checkin-counts/#{year}/"
  $.ajax
    url: url,
    dataType: "json",
    success: (data, status, xhr) ->
      $(domId).html ""
      calendar_heatmap.create
        missing_as_zero: true,
        target: domId,
        data: data,
        date_var: "day",
        fill_var: "count",
        missing_as_zero: true,
        title: "打卡记录 (#{year})",
        color_scheme: ["rgb(237,237,237)", "rgb(217,239,139)","rgb(217,239,139)","rgb(217,239,139)", "rgb(217,239,139)", "rgb(166,217,106)", "rgb(102,189,99)", "rgb(26,152,80)", "rgb(0,104,55)", "rgb(99, 121, 57)", "rgb(59, 100, 39)"],
        stroke_color: "whitesmoke",
        legend_title: "连续打卡天数",
        on_click: (d) -> console.log(d)
    error: (xhr, status, err) ->
      console.error(url, status, err.toString())

updateCheckinCounts(2015)
