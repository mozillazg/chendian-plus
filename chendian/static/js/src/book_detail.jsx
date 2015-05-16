var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';

var BookInfo = React.createClass({
  initEditable: function() {
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
  },

  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
        // bind editable
        this.initEditable();
        // reader count
        $('#reader-count').html(data.reader_count);

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
    var book = this.state.data;
    book.author = book.author || 'author';
    book.isbn = book.isbn || 'isbn';
    book.douban_url = book.douban_url || 'douban_url';
    book.description = book.description || 'description';
    var url = '/b/' + book.id;
    var bookInfo = (
        <div>
          <div className="cover text-center col-md-6">
            <a href={url}>
              <img className="img-rounded"
                alt={book.name} src={book.cover} title={book.name} id="book-cover"/>
            </a>
          </div>
          <div className="detail col-md-6">
            <ul className="list-unstyled">
              <li>名称：<span className="editable" data-type="text" data-name="name">{book.name}</span></li>
              <li>作者：<span className="editable" data-type="text" data-name="author">{book.author}</span></li>
              <li>ISBN: <span className="editable" data-type="text" data-name="isbn">{book.isbn}</span></li>
              <li>豆瓣: <span className="editable" data-type="url" data-name="douban_url" data-value={book.douban_url}>{book.douban_url}</span>
              </li>
            </ul>
          </div>
          <div className="description col-md-12">
          <div className="editable" data-name="description"
           data-value={book.description} data-type="textarea">{book.description}</div>
          </div>
        </div>
      );
    return (
      <div className="book-info">
        {bookInfo}
      </div>
    );
  }
});

React.render(
  <BookInfo url={bookURL} />,
  document.getElementById('content')
);

var checkinsURL = bookURL + 'checkins/';
React.render(
  <CheckinList url={checkinsURL} per_page="30" />,
  document.getElementById('checkin-list')
);
