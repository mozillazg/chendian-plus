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
    var bookNodes = this.state.data.map(function (book) {
      return (
        React.createElement(Book, {book: book, key: book.id}
        )
      )
    });
    return (
      React.createElement("div", null, 
        React.createElement("ul", {className: "list-inline book-list"}, 
          bookNodes
        ), 

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

React.render(
  React.createElement(BookList, {url: "/api/books/", per_page: "30"}),
  document.getElementById('content')
);
