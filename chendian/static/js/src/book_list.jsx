var Book = React.createClass({
  initPopover: function(component) {
    if (isMobile.any) {return}

    var $this = $(React.findDOMNode(component));
    $this.popover({
      trigger: 'hover',
      html: true,
      delay: {"show": 300, "hide": 300},
      container: 'body',
      template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-content"></div></div>',
      content: function() {
        if ($this.popoverHtml) {
          return $this.popoverHtml;
        }
        var html = '<ul class="list-unstyled">';
        var id = $this.data('id');
        $.ajax({
          url: '/api/books/' + id + '/',
          async: false,
          cache: true,
          success: function(data) {
            var desc = data.description;
            var max_word = 50;
            if (desc.length > max_word) {
              desc = desc.slice(0, max_word) + '...';
            }
            html += '<li>名称：' + escapeHtml(data.name) + '</li>';
            html += '<li>作者：' + escapeHtml(data.author) + '</li>';
            html += '<li>简介：' + escapeHtml(desc) + '</li>';
            html += '</ul>';
            $this.popoverHtml = html;
          }
        });
        return html
      }
    });
  },

  handleMouseOver: function(event) {
    $this = $(event.target);
    $this.popover('show');
  },

  render: function() {
    var book = this.props.book;
    var url = '/b/' + book.id + '/';
    return (
      <li className="book list-unstyled" data-id={book.id} ref={this.initPopover}>
        <a href={url}>
          <img className="img-rounded"
            alt={book.name} src={book.cover}/>
          <span className="well well-sm" title={book.name}>{book.name}</span>
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
React.render(
  <BookList url={url} per_page={perPage} />,
  document.getElementById('content')
);
