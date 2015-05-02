var Book = React.createClass({displayName: "Book",
  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      React.createElement("li", {className: "book", "data-author": "", "data-desc": book.description}, 
        React.createElement("a", {href: url}, 
          React.createElement("img", {"data-src": "holder.js/160x180", className: "img-rounded", 
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

React.render(
  React.createElement(BookList, {url: "/api/books/"}),
  document.getElementById('content')
);
