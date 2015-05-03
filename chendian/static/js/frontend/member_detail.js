var MemberInfo = React.createClass({displayName: "MemberInfo",
  loadDataFromServer: function() {
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

  getInitialState: function() {
    return {data: {}};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    var member = this.state.data;
    member.nick_name = member.nick_name || 'nick_name';
    member.description = member.description || 'description';
    var url = '/m/' + member.id;
    var memberInfo = (
      React.createElement("div", {className: "member"}, 
        React.createElement("div", {className: "avatar-120 col-md-5"}, 
          React.createElement("a", {href: url}, 
            React.createElement("img", {"data-src": "holder.js/120x120/random", className: "img-rounded", 
              alt: member.nick_name, style: {width: "120px", height: "120px"}, 
              src: member.avatar, title: member.nick_name, id: "member-avatar"})
          )
        ), 
        React.createElement("div", {className: "detail col-md-7"}, 
          React.createElement("ul", {className: "list-unstyled"}, 
            React.createElement("li", null, "编号: ", React.createElement("span", null, member.sn)), 
            React.createElement("li", null, "昵称: ", React.createElement("span", {className: "editable", "data-name": "nick_name", 
                        "data-value": member.nick_name, "data-type": "text"
                      }, member.nick_name))
          )
        )
      )
      );
    return (
      React.createElement("div", {className: "member-info"}, 
        memberInfo, 
        React.createElement("div", {className: "description col-md-12"}, 
          React.createElement("div", {className: "editable", "data-name": "description", 
           "data-value": member.description, "data-type": "textarea"}, member.description)
        )
      )
    );
  }
});

var Book = React.createClass({displayName: "Book",
  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      React.createElement("li", {className: "book", "data-author": "", "data-desc": book.description}, 
        React.createElement("a", {href: url}, 
          React.createElement("img", {"data-src": "holder.js/200x288", className: "img-rounded", 
            alt: book.name, src: book.cover, title: book.name}), 
          React.createElement("span", {className: "well well-sm"}, book.name)
        )
      )
    );
  }
});

var BookList = React.createClass({displayName: "BookList",
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
    var bookNodes = this.state.data.map(function (book) {
      return (
        React.createElement(Book, {book: book, key: book.id}
        )
      )
    });
    return (
      React.createElement("ul", {className: "list-inline book-list"}, 
        bookNodes
      )
    );
  }
});


var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';
var initEditable = function() {
  $('.member-info .editable').editable({
    url: memberURL,
    pk: memberID,
    autotext: 'always',
    validate: function(value) {
      if($.trim(value) == '') {
        return 'This field is required';
      }
    }
  });
};
React.render(
  React.createElement(MemberInfo, {url: memberURL}),
  document.getElementById('profile'),
  function() {
    if ($("#profile").data('editable')) {
      initEditable();
    }
  }
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  React.createElement(CheckinList, {url: checkinsURL, per_page: "30"}),
  document.getElementById('checkin-list')
);


var booksURL = memberURL + 'books/';
React.render(
  React.createElement(BookList, {url: booksURL}),
  document.getElementById('read-books')
);
