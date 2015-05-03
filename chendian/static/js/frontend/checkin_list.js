var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    var checkin = this.props.checkin;
    var sn = checkin.sn || '';
    var url = '/m/sn/' + sn.toString();
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
  loadDataFromServer: function() {
    var page = this.state.page || 1;
    $.ajax({
      url: this.props.url,
      data: {
        'page': page,
        'per_page': this.props.per_page
      },
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handlePerPageClick: function(event) {
    var page = this.state.page - 1 || 1;
    this.setState({page: page}, function() {
        this.loadDataFromServer();
    }.bind(this));
  },

  handleNextPageClick: function(event) {
    var page = this.state.page + 1 || 1;
    this.setState({page: page}, function() {
        this.loadDataFromServer();
    }.bind(this));
  },

  getInitialState: function() {
    return {data: [], page: 1};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    var checkinNodes = this.state.data.map(function (checkin) {
      var think = checkin.think.replace('\n', '<br />');
      var bookURL = '/b/name/' + checkin.book_name;
      return (
        React.createElement(Checkin, {checkin: checkin, key: checkin.id}, 
          "#打卡 ", React.createElement("a", {href: bookURL}, "《", checkin.book_name, "》"), " ", think
        )
      )
    });
    return (
      React.createElement("div", null, 
        checkinNodes, 
        React.createElement("nav", null, 
          React.createElement("ul", {className: "pager"}, 
            React.createElement("li", {className: "previous"}, React.createElement("a", {href: "#", onClick: this.handlePerPageClick}, 
                React.createElement("span", {"aria-hidden": "true"}, "←"), " Previous")), 
            React.createElement("li", null, React.createElement("span", {className: "text-center"}, "第 ", this.state.page, " 页")), 
            React.createElement("li", {className: "next"}, React.createElement("a", {href: "#", onClick: this.handleNextPageClick}, 
                "Next ", React.createElement("span", {"aria-hidden": "true"}, "→")))
          )
        )
      )
    );
  }
});
