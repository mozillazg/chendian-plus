var BookInfo = React.createClass({displayName: "BookInfo",
  getInitialState: function() {
    return {data: {}};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var book = this.state.data;
    var bookInfo = (
        React.createElement("div", null, 
          React.createElement("h1", null, book.name), 
          React.createElement("div", {className: "book-description"}, 
            book.description
          )
        )
      );
    return (
      React.createElement("div", {className: "bookInfo"}, 
        bookInfo
      )
    );
  }
});

var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          "【", this.props.sn, "】", this.props.nickName, " ", this.props.date
        ), 
        React.createElement("div", {className: "checkin-content"}, 
          this.props.children
        )
      )
    );
  }
});

var CheckinList = React.createClass({displayName: "CheckinList",
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var checkinNodes = this.state.data.map(function (checkin) {
    var think = checkin.think.replace('\n', '<br />');
      return (
        React.createElement(Checkin, {sn: checkin.sn, nickName: checkin.nick_name, 
          date: checkin.posted_at}, 
          "#打卡 《", checkin.book_name, "》", think
        )
      )
    });
    return (React.createElement("div", null, checkinNodes));
  }
});

var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';
React.render(
  React.createElement(BookInfo, {url: bookURL}),
  document.getElementById('content')
);

var checkinsURL = bookURL + 'checkins/';
React.render(
  React.createElement(CheckinList, {url: checkinsURL}),
  document.getElementById('checkin-list')
);
