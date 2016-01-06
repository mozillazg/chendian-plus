
var Book = React.createClass({
  initPopover: function(component) {
    if (isMobile.any) {return}

    var $this = $(ReactDOM.findDOMNode(component));
    var id = $this.data('id');
    var url = '/api/books/' + id + '/';

    $this.webuiPopover({
      type: "async",
      url: url,
      trigger: "hover",
      placement: "horizontal",
      delay: {show: 100, hide: 300},
      content: function(data) {
        if ($this.popoverHtml) {
          return $this.popoverHtml;
        }
        var html = '<div class="" role="tooltip"><div class="arrow"></div><div class="popover-content">';
        var desc = data.description;
        var maxWord = 50;
        if (desc.length > maxWord) {
          desc = desc.slice(0, maxWord) + '...';
        }
        html += '<ul class="list-unstyled">';
        html += '<li>名称：' + escapeHtml(data.name) + '</li>';
        html += '<li>作者：' + escapeHtml(data.author) + '</li>';
        html += '<li>简介：' + escapeHtml(desc) + '</li>';
        html += '</ul>';
        html += '</div></div>';
        $this.popoverHtml = html;
        return html
      }
    });
  }.bind(this),

  // handleMouseOver: function(event) {
  //   $this = $(event.target);
  //   $this.popover('show');
  // },

  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      <li className="book list-unstyled" data-id={book.id} ref={this.initPopover}>
        <a href={url} title={book.name}>
          <img className="img-rounded lazyload"
            alt={book.name} src={book.cover} data-src={book.cover} />
          <span className="well well-sm">{book.name}</span>
        </a>
      </li>
    );
  }
});

var BookList = React.createClass({
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    var bookNodes = this.state.data.map(function (book) {
      return (
        <Book book={book} key={book.id}>
        </Book>
      )
    });
    return (
      <div>
        <ul className="book-list">
          {bookNodes}
        </ul>

        <nav>
          <ul className="pager clearfix">
            <li className="previous"><a href="javascript: void(0);" onClick={this.handlePerPageClick}>
                <span aria-hidden="true">&larr;</span> Previous</a></li>
            <li><span className="text-center">第 {this.state.page} / {this.state.max_page} 页</span></li>
            <li className="next"><a href="javascript: void(0);" onClick={this.handleNextPageClick}>
                Next <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </nav>
      </div>
    );
  }
});

var url = '/api/books/?_fields=id,cover,name';
var perPage = isMobile.any ? 20 : 100;
ReactDOM.render(
  <BookList url={url} per_page={perPage} />,
  document.getElementById('content')
);
