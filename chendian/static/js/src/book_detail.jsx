var bookID = $('#content').data('id');
var editable = $("#content").data("editable");
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

  newTagHandler: function(event) {
    var tagName = prompt("请输入新标签名称");
    if (!tagName || tagName.trim() === "") {
      return false;
    }
    var url = this.props.bookURL + "tags/new";
    $.ajax({
      url: url,
      method: "POST",
      data: JSON.stringify({
        "name": tagName
      }),
      dataType: 'json',
      success: function(data) {
        var book = this.state.data;
        book.tags = book.tags || [];
        book.tags.push(data);
        this.setState({data: book});
        alert('success');
      }.bind(this)
    });
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
    var _tags = book.tags || [];
    var tags = _tags.map(function (tag) {
      var url = "/b/?tags__name=" + tag.name;
      return (
        <li key={tag.id} className="label tag pull-left">
          <a href={url}>{tag.name}</a>
        </li>
      )
    });
    var newTagButton = function() {
      if (this.props.editable) {
        return (
          <li class="tag pull-left">
            <a href="javascript: void(0);" onClick={this.newTagHandler}>
              <span className="glyphicon glyphicon-plus-sign" aria-hidden="true"
              title="新增标签"></span>
            </a>
          </li>
        )
      } else {return ""}
    }.bind(this)();

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
              <li>标签:
              </li>
            </ul>
          </div>
          <div className="col-md-6 tags">
            <ul className="list-inline">
              {tags} {newTagButton}
            </ul>
          </div>
          <div className="description col-md-12 clearfix">
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
  <BookInfo bookURL={bookURL} url={bURL} bookId={bookID}
   editable={editable} />,
  document.getElementById('content')
);

var checkinsURL = bookURL + 'checkins/';
var perPage = isMobile.any ? 10 : 20;
ReactDOM.render(
  <CheckinList url={checkinsURL} per_page={perPage} />,
  document.getElementById('checkin-list')
);

var notesURL = bookURL + 'hundred-goal-notes/';
var perPage = isMobile.any ? 5 : 10;
ReactDOM.render(
  <Notes url={notesURL} per_page={perPage} pageKey='np' />,
  document.getElementById('hundred-goal-notes')
);
