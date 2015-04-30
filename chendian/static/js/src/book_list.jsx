var Book = React.createClass({
  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      <li className="book" data-author="" data-desc={book.description}>
        <a href={url}>
          <img data-src="holder.js/160x160" className="img-rounded"
            alt="160x160" style={{width: "160px", height: "160px"}}
            src="" title={book.name}/>
        </a>
        <div className="well well-sm">{book.name}</div>
      </li>
    );
  }
});

var BookList = React.createClass({
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
        <Book book={book}>
        </Book>
      )
    });
    return (
      <ul className="list-inline book-list">
        {bookNodes}
      </ul>
    );
  }
});

React.render(
  <BookList url='/api/books/' />,
  document.getElementById('content')
);
