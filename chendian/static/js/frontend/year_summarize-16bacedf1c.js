var year = $('.year-top').data('year');
var member_id = $('.year-top').data('member-id');


var BookRaw = React.createClass({displayName: "BookRaw",
  render: function() {
    var book = this.props.top_book.book;
    var count = this.props.top_book.reader_count;
    var url = '/b/' + book.id + '/';
    return (
      React.createElement("tr", null, 
        React.createElement("td", null, React.createElement("a", {href: url, title: book.name}, book.name)), 
        React.createElement("td", null, count)
      )
    );
  }
});

var BooksTable = React.createClass({displayName: "BooksTable",
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
    return {data: []};
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
    var BookNodes = this.state.data.map(function (top_book) {
      return (
        React.createElement(BookRaw, {top_book: top_book, key: top_book.id}
        )
      )
    });
    return (
      React.createElement("table", {className: "table table-striped table-bordered table-hover"}, 
        React.createElement("thead", null, 
          React.createElement("tr", null, 
            React.createElement("th", null, "名称"), 
            React.createElement("th", null, "读者数（人）")
          )
        ), 
        React.createElement("tbody", null, 
            BookNodes
        )
      )
    );
  }
});

var ReaderRaw = React.createClass({displayName: "ReaderRaw",
  render: function() {
    var reader = this.props.reader;
    var url = '/m/' + reader.member.id + '/';
    return (
      React.createElement("tr", null, 
        React.createElement("td", null, React.createElement("a", {href: url, title: reader.member.nick_name}, reader.member.nick_name)), 
        React.createElement("td", null, reader.count)
      )
    );
  }
});

var ReadersTable = React.createClass({displayName: "ReadersTable",
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
    return {data: []};
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
    var readerNodes = this.state.data.map(function (reader) {
      return (
        React.createElement(ReaderRaw, {reader: reader, key: reader.id}
        )
      )
    });
    return (
      React.createElement("table", {className: "table table-striped table-bordered table-hover"}, 
        React.createElement("thead", null, 
          React.createElement("tr", null, 
            React.createElement("th", null, "昵称"), 
            React.createElement("th", null, "数量（本）")
          )
        ), 
        React.createElement("tbody", null, 
            readerNodes
        )
      )
    );
  }
});


var MineBookRaw = React.createClass({displayName: "MineBookRaw",
  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      React.createElement("li", null, 
        React.createElement("a", {href: url, title: book.name}, book.name)
      )
    );
  }
});

var MineBookList = React.createClass({displayName: "MineBookList",
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
    return {data: []};
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
    } else {
        $("#mine-book-count").text("（" + this.state.data.length + " 本）");
    }
    var BookNodes = this.state.data.map(function (book) {
      return (
        React.createElement(MineBookRaw, {book: book, key: book.id}
        )
      )
    });
    return (
      React.createElement("ul", null, BookNodes)
    );
  }
});

var topBookURL = '/api/books/year/' + year + '/top/20/';
ReactDOM.render(
  React.createElement(BooksTable, {url: topBookURL}),
  document.getElementById('year-top-books')
);

var topReaderURL = topBookURL + 'readers/';
ReactDOM.render(
  React.createElement(ReadersTable, {url: topReaderURL}),
  document.getElementById('year-top-readers')
);

if (member_id) {
    var mineBooksURL = '/api/members/' + member_id + '/year/' + year + '/books/'
    ReactDOM.render(
      React.createElement(MineBookList, {url: mineBooksURL}),
      document.getElementById('year-mine-books')
    );
}
