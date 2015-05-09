var Book = React.createClass({
  initPopover: function(component) {
    var $this = $(React.findDOMNode(component));
    $this.popover({
      trigger: 'hover',
      html: true,
      delay: {"show": 100, "hide": 100},
      container: 'body',
      template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-content"></div></div>',
      content: function() {
        var html = '<ul class="list-unstyled">';
        html += '<li>名称：' + $this.data('name') + '</li>';
        html += '<li>作者：' + $this.data('author') + '</li>';
        html += '<li>简介：' + $this.data('desc') + '</li>';
        html += '</ul>';
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
      <li className="book" data-author={book.author}
        data-name={book.name} data-desc={book.description}
        ref={this.initPopover}>
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
        <Book book={book} key={book.id}>
        </Book>
      )
    });
    return (
      <div>
        <ul className="list-inline book-list">
          {bookNodes}
        </ul>

        <nav>
          <ul className="pager">
            <li className="previous"><a href="javascript: void(0);" onClick={this.handlePerPageClick}>
                <span aria-hidden="true">&larr;</span> Previous</a></li>
            <li><span className="text-center">第 {this.state.page} 页</span></li>
            <li className="next"><a href="javascript: void(0);" onClick={this.handleNextPageClick}>
                Next <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </nav>
      </div>
    );
  }
});

React.render(
  <BookList url='/api/books/' per_page="100" />,
  document.getElementById('content')
);
