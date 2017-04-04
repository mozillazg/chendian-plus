
var ArticleList = React.createClass({displayName: "ArticleList",
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    var ArticleNodes = this.state.data.map(function (article) {
      return (
        React.createElement(Article, {key: article.id, article: article}
        )
      )
    });
    return (
      React.createElement("div", null, 
        ArticleNodes, 
        React.createElement("nav", null, 
          React.createElement("ul", {className: "pager"}, 
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

var url = '/api/blog/articles/';
var perPage = isMobile.any ? 5 : 10;
ReactDOM.render(
  React.createElement(ArticleList, {url: url, per_page: perPage}),
  document.getElementById('article-list')
);
