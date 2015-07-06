var Article = React.createClass({
  render: function() {
    var article = this.props.article;
    var author = article.author || {nick_name: '', id: 0};
    var _tags = article.tags || [];
    var _categories = article.categories || [];
    var author_url = "/m/" + author.id;
    var title_url = "/a/" + article.id;

    var tags = _tags.map(function (tag) {
      return (
        <span key={tag.id} className="label label-primary">{tag.name}</span>
      )
    });
    var categories = _categories.map(function (category) {
      return (
        <span key={category.id} className="label label-primary">{category.name}</span>
      )
    });

    return (
      <div className="col-md-12 article-list">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h2><a href={title_url}>{article.title}</a></h2>
            <div>
              <ul className="list-inline">
                <li>
                  <a className="label label-primary" href={author_url}>
                    {author.nick_name}
                  </a>
                  于 {article.created_at} 发布
                </li>
                <li>tags: {tags}</li>
                <li>categories: {categories}</li>
              </ul>
            </div>
          </div>
          <div className="panel-body">
            <div dangerouslySetInnerHTML={{__html: article.content}} />
          </div>
          <div className="panel-footer clearfix"></div>
        </div>
      </div>
    );
  }
});
