var Tag = React.createClass({
  render: function() {
    var tag = this.props.tag;
    return (
      <li>{tag.name}</li>
    )
  }
});

var Category = React.createClass({
  render: function() {
    var category = this.props.category;
    return (
      <li>{category.name}</li>
    )
  }
});

var Article = React.createClass({
  render: function() {
    var article = this.props.article;
    var author = article.author
    if (!author) {
      author = {
        nick_name: '',
        id: 0
      }
    }
    var author_url = "/m/" + author.id;
    var tags = article.tags.map(function (tag) {
      return (
        <span className="label label-primary">{tag.name}</span>
      )
    });
    var categories = article.categories.map(function (category) {
      return (
        <span className="label label-primary">{category.name}</span>
      )
    });

    return (
      <div className="col-md-12 article-list">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h2>{article.title}</h2>
            <div>
              <ul className="list-inline">
                <li><a className="label label-primary" href={author_url}>{author.nick_name}</a>
                  于 {article.created_at} 发布</li>
                <li>tags: {tags}</li>
                <li>categories: {categories}</li>
              </ul>
            </div>
          </div>
          <div className="panel-body">
            <div dangerouslySetInnerHTML={{__html: article.content}}></div>
          </div>
          <div className="panel-footer clearfix"></div>
        </div>
      </div>
    );
  }
});

var ArticleList = React.createClass({
  mixins: [PaginationMixin],

  render: function() {
    var ArticleNodes = this.state.data.map(function (article) {
      return (
        <Article article={article}>
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

var url = '/api/blog/articles';
React.render(
  <ArticleList url={url} per_page="10" />,
  document.getElementById('article-list')
);
