var updateCheckinCounts;

updateCheckinCounts = function(year) {
  var domId, id, url;
  if (isMobile.any) {
    return;
  }
  domId = "#checkin-count";
  id = $(domId).data("id");
  year = (new Date()).getFullYear();
  url = "/api/members/" + id + "/checkin-counts/" + year + "/";
  return $.ajax({
    url: url,
    dataType: "json",
    success: function(data, status, xhr) {
      var chartData, heatmap;
      chartData = data.map(function(item) {
        var date, obj;
        obj = {};
        date = new Date(item.date);
        obj.date = date;
        obj.count = item.count;
        return obj;
      });
      $(domId).html("");
      heatmap = calendarHeatmap().data(chartData).selector(domId).tooltipEnabled(true).legendEnabled(true).tooltipUnit('counts').colorRange(["rgb(237,237,237)", "rgb(217,239,139)", "rgb(166,217,106)", "rgb(102,189,99)", "rgb(26,152,80)", "rgb(0,104,55)", "rgb(99, 121, 57)"]).onClick(function(data) {});
      return heatmap();
    },
    error: function(xhr, status, err) {
      return console.error(url, status, err.toString());
    }
  });
};

updateCheckinCounts();
