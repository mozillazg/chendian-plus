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
    book.author = book.author || 'author';
    book.isbn = book.isbn || 'isbn';
    book.douban_url = book.douban_url || 'douban_url';
    book.description = book.description || 'description';
    var url = '/b/' + book.id;
    var bookInfo = (
        React.createElement("div", null, 
          React.createElement("div", {className: "cover text-center col-md-5"}, 
            React.createElement("a", {href: url}, 
              React.createElement("img", {className: "img-rounded", 
                alt: book.name, src: book.cover, title: book.name, id: "book-cover"})
            )
          ), 
          React.createElement("div", {className: "detail col-md-7"}, 
            React.createElement("ul", {className: "list-unstyled"}, 
              React.createElement("li", null, "名称：", React.createElement("span", {className: "editable", "data-type": "text", "data-name": "name"}, book.name)), 
              React.createElement("li", null, "作者：", React.createElement("span", {className: "editable", "data-type": "text", "data-name": "author"}, book.author)), 
              React.createElement("li", null, "ISBN: ", React.createElement("span", {className: "editable", "data-type": "text", "data-name": "isbn"}, book.isbn)), 
              React.createElement("li", null, "豆瓣: ", React.createElement("span", {className: "editable", "data-type": "url", "data-name": "douban_url", "data-value": book.douban_url}, book.douban_url)
              )
            )
          ), 
          React.createElement("div", {className: "description col-md-12"}, 
          React.createElement("div", {className: "editable", "data-name": "description", 
           "data-value": book.description, "data-type": "textarea"}, book.description)
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

var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';
var initEditable = function() {
  $('.book-info .editable').editable({
    url: bookURL,
    pk: bookID,
    // autotext: 'always',
    validate: function(value) {
      if($.trim(value) == '') {
        return 'This field is required';
      }
    }
  });
};
React.render(
  React.createElement(BookInfo, {url: bookURL}),
  document.getElementById('content'),
  function() {initEditable();}
);

var checkinsURL = bookURL + 'checkins/';
React.render(
  React.createElement(CheckinList, {url: checkinsURL, per_page: "30"}),
  document.getElementById('checkin-list')
);
