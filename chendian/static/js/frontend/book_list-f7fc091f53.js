
var Book = React.createClass({displayName: "Book",
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
      React.createElement("li", {className: "book list-unstyled", "data-id": book.id, ref: this.initPopover}, 
        React.createElement("a", {href: url, title: book.name}, 
          React.createElement("img", {className: "img-rounded lazyload", 
            alt: book.name, src: book.cover, "data-src": book.cover}), 
          React.createElement("span", {className: "well well-sm"}, book.name)
        )
      )
    );
  }
});

var BookList = React.createClass({displayName: "BookList",
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    var bookNodes = this.state.data.map(function (book) {
      return (
        React.createElement(Book, {book: book, key: book.id}
        )
      )
    });
    return (
      React.createElement("div", null, 
        React.createElement("ul", {className: "book-list"}, 
          bookNodes
        ), 

        React.createElement("nav", null, 
          React.createElement("ul", {className: "pager clearfix"}, 
            React.createElement("li", {className: "previous"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handlePerPageClick}, 
                React.createElement("span", {"aria-hidden": "true"}, "←"), " Previous")), 
            React.createElement("li", null, React.createElement("span", {className: "text-center"}, "第 ", this.state.page, " / ", this.state.max_page, " 页")), 
            React.createElement("li", {className: "next"}, React.createElement("a", {href: "javascript: void(0);", onClick: this.handleNextPageClick}, 
                "Next ", React.createElement("span", {"aria-hidden": "true"}, "→")))
          )
        )
      )
    );
  }
});

var url = '/api/books/?_fields=id,cover,name';
var perPage = isMobile.any ? 20 : 100;
ReactDOM.render(
  React.createElement(BookList, {url: url, per_page: perPage}),
  document.getElementById('content')
);
