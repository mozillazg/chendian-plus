var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';

var BookInfo = React.createClass({

  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
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
    var default_douban_url = 'http://book.douban.com/subject_search?search_text=' + book.name;
    book.douban_url = book.douban_url || default_douban_url;
    book.description = filterXSS(book.description);
    book.description = book.description ? book.description.replace(/\r\n/g, '<br />') : '';
    book.description = book.description.replace(/\n/g, '<br />');
    var url = '/b/' + book.id;
    var bookInfo = (
        <div>
          <div className="cover text-center col-md-6">
            <a href={url}>
              <img className="img-rounded"
                alt={book.name} src={book.cover} title={book.name} id="book_cover"/>
            </a>
          </div>
          <div className="detail col-md-6">
            <ul className="list-unstyled">
              <li>名称：<span id="book_name">{book.name}</span></li>
              <li>作者：<span id="book_author">{book.author}</span></li>
              <li>ISBN: <span id="book_isbn">{book.isbn}</span></li>
              <li>豆瓣页面: <a id="book_douban_url" href={book.douban_url} target="_blank">查看</a>
              </li>
            </ul>
          </div>
          <div className="description col-md-12">
            <div id="book_description" dangerouslySetInnerHTML={{__html: book.description }}></div>
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
