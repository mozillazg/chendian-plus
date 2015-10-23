var bookID = $('#content').data('id');
var bookURL = '/api/books/' + bookID + '/';

var BookInfo = React.createClass({

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

  loading: function() {
    return (
      <div dangerouslySetInnerHTML={{__html: loadingDiv()}} />
    )
  },
  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    var book = this.state.data;
    var default_douban_url = 'http://book.douban.com/subject_search?search_text=' + book.name;
    book.douban_url = book.douban_url || default_douban_url;
    book.description = filterXSS(book.description);
    book.description = newline2p(book.description);
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

var bURL = bookURL + '?_extend=reader_count';
ReactDOM.render(
  <BookInfo url={bURL} />,
  document.getElementById('content')
);

var checkinsURL = bookURL + 'checkins/';
var perPage = isMobile.any ? 10 : 20;
ReactDOM.render(
  <CheckinList url={checkinsURL} per_page={perPage} />,
  document.getElementById('checkin-list')
);
