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
          React.createElement("div", {className: "bookDescription"}, 
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

var Think = React.createClass({displayName: "Think",
  render: function() {
    return (
      React.createElement("div", {className: "think"}, 
        React.createElement("div", {className: "think-author"}, 
          "【", this.props.sn, "】", this.props.nickName, "(", this.props.qq, ") ", this.props.date
        ), 
        React.createElement("div", {className: "think-content"}, 
          this.props.children
        )
      )
    );
  }
});

var ThinkList = React.createClass({displayName: "ThinkList",
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
    var thinkNodes = this.state.data.map(function (think) {
      return (
        React.createElement(Think, {sn: think.sn, qq: think.qq, nickName: think.nick_name, date: think.posted_at}, 
          think.think
        )
      )
    });
    return (
      React.createElement("div", {className: "panel panel-default"}, 
        React.createElement("div", {className: "panel-heading"}, "阅读记录"), 
        React.createElement("div", {className: "panel-body"}, 
          thinkNodes
        ), 
        React.createElement("div", {className: "panel-footer clearfix"})
      )
    );
  }
});

var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';
React.render(
  React.createElement(BookInfo, {url: bookURL}),
  document.getElementById('content')
);

var thinksURL = bookURL + 'thinks/';
React.render(
  React.createElement(ThinkList, {url: thinksURL}),
  document.getElementById('thinkList')
);
