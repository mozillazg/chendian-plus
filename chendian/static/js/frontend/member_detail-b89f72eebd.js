var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';

var MemberInfo = React.createClass({displayName: "MemberInfo",
  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data) {
        this.setState({data: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  getInitialState: function() {
    return {data: {}};
  },
  loading: function() {
    return (
      React.createElement("div", {dangerouslySetInnerHTML: {__html: loadingDiv()}})
    )
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var member = this.state.data;
    member.nick_name = member.nick_name || 'nick_name';
    member.description = member.description || 'description';
    var url = '/m/' + member.id + '/';
    var memberInfo = (
      React.createElement("div", {className: "member"}, 
        React.createElement("div", {className: "avatar-120 col-md-5 avatar"}, 
          React.createElement("a", {href: url, title: member.nick_name}, 
            React.createElement("img", {className: "img-rounded", 
              alt: member.nick_name, style: {width: "120px", height: "120px"}, 
              src: member.avatar, id: "member-avatar"})
          )
        ), 
        React.createElement("div", {className: "detail col-md-7"}, 
          React.createElement("ul", {className: "list-unstyled"}, 
            React.createElement("li", null, "编号: ", React.createElement("span", null, member.sn)), 
            React.createElement("li", null, "昵称: ", React.createElement("span", {id: "member-nick-name"}, member.nick_name))
          )
        )
      )
      );
    return (
      React.createElement("div", {className: "member-info"}, 
        memberInfo, 
        React.createElement("div", {className: "description col-md-12"}, 
          React.createElement("div", {id: "member-description"}, member.description)
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
        React.createElement("a", {href: url, title: book.name}, 
          React.createElement("img", {className: "img-rounded", 
            alt: book.name, src: book.cover}), 
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
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data, status, xhr) {
        this.setState({data: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loading: function() {
    return (
      React.createElement("div", {dangerouslySetInnerHTML: {__html: loadingDiv()}})
    )
  },
  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    if (this.state.count) {
      $("#read_count").text("（" + this.state.count + " 本）");
    }
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

ReactDOM.render(
  React.createElement(MemberInfo, {url: memberURL}),
  document.getElementById('profile')
);

var checkinsURL = memberURL + 'checkins/';
var perPage = isMobile.any ? 3 : 5;
ReactDOM.render(
  React.createElement(CheckinList, {url: checkinsURL, per_page: perPage}),
  document.getElementById('checkin-list')
);


var booksURL = memberURL + 'books/?_fields=id,name,cover';
ReactDOM.render(
  React.createElement(BookList, {url: booksURL}),
  document.getElementById('read-books')
);
