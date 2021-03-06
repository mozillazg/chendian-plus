
var ArticleList = React.createClass({
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    var ArticleNodes = this.state.data.map(function (article) {
      return (
        <Article key={article.id} article={article}>
        </Article>
      )
    });
    return (
      <div>
        {ArticleNodes}
        <nav>
          <ul className="pager">
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

var url = '/api/blog/articles/';
var perPage = isMobile.any ? 5 : 10;
ReactDOM.render(
  <ArticleList url={url} per_page={perPage} />,
  document.getElementById('article-list')
);
