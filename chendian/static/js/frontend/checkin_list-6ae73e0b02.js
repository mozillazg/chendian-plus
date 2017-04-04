
var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    var checkin = this.props.checkin;
    var sn = checkin.sn || '';
    var url = '/m/sn/' + sn.toString() + '/';
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          React.createElement("a", {href: url}, "【", sn, "】", checkin.nick_name), 
          React.createElement("span", {className: "time"}, checkin.posted_at)
        ), 
        React.createElement("div", {className: "checkin-content"}, 
          this.props.children
        )
      )
    );
  }
});

var CheckinList = React.createClass({displayName: "CheckinList",
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var checkinNodes = this.state.data.map(function (checkin) {
      var think = newline2br(filterXSS(checkin.think));
      var bookURL = '/b/name/' + checkin.book_name + '/';
      return (
        React.createElement(Checkin, {checkin: checkin, key: checkin.id}, 
          "#打卡 ", React.createElement("a", {href: bookURL}, "《", checkin.book_name, "》"), 
          React.createElement("span", {dangerouslySetInnerHTML: {__html: think}})
        )
      )
    });
    return (
      React.createElement("div", null, 
        checkinNodes, 
        React.createElement("nav", null, 
          React.createElement("ul", {className: "pager"}, 
            React.createElement("li", {className: "previous"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handlePerPageClick}, 
                React.createElement("span", {"aria-hidden": "true"}, "←"), " Previous")), 
            React.createElement("li", null, React.createElement("span", {className: "text-center"}, "第 ", this.state.page, " / ", this.state.max_page, " 页")), 
            React.createElement("li", {className: "next"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handleNextPageClick}, 
                "Next ", React.createElement("span", {"aria-hidden": "true"}, "→")))
          )
        )
      )
    );
  }
});
