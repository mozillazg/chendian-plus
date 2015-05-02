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
    var url = '/b/' + book.id;
    var bookInfo = (
        React.createElement("div", null, 
          React.createElement("div", {className: "cover text-center col-md-6"}, 
            React.createElement("a", {href: url}, 
              React.createElement("img", {"data-src": "holder.js/160x180/random", className: "img-rounded", 
                alt: book.name, style: {width: "160px", height: "180px"}, 
                src: book.cover, title: book.name})
            )
          ), 
          React.createElement("div", {className: "detail col-md-6"}, 
            React.createElement("ul", {className: "list-unstyled"}, 
              React.createElement("li", null, "名称：", book.name), 
              React.createElement("li", null, "作者：", book.author), 
              React.createElement("li", null, "ISBN: ", book.isbn), 
              React.createElement("li", null, "豆瓣: ", React.createElement("a", {href: book.douban_url, target: "_blank"}, "Go to douban"))
            )
          ), 
          React.createElement("div", {className: "description col-md-12"}, 
            book.description
          )
        )
      );
    return (
      React.createElement("div", {className: "book-info"}, 
        bookInfo
      )
    );
  }
});

var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    var checkin = this.props.checkin;
    var sn = checkin.sn || '';
    var url = '/m/sn/' + sn.toString();
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          React.createElement("a", {href: url}, "【", sn, "】", checkin.nickName), 
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
        React.createElement(Checkin, {checkin: checkin, key: checkin.id}, 
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
