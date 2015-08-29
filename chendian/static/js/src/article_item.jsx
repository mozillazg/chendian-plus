var Article = React.createClass({
  render: function() {
    var article = this.props.article;
    var author = article.author || {nick_name: '', id: 0};
    var _tags = article.tags || [];
    var _categories = article.categories || [];
    var author_url = "/a/?author__nick_name=" + encodeURIComponent(author.nick_name);
    var title_url = "/a/" + article.id;
    var whiteList = $.extend({}, filterXSS.whiteList);
    whiteList.span = ['style'];
    var content = filterXSS(article.content, {whiteList: whiteList});

    var tags = _tags.map(function (tag) {
      var url = "/a/?tags__slug=" + tag.slug;
      return (
        <span key={tag.id} className="">
          <a href={url}>{tag.name}</a>
        </span>
      )
    });
    var categories = _categories.map(function (category) {
      var url = "/a/?categories__slug=" + category.slug;
      return (
        <span key={category.id} className="">
          <a href={url}>{category.name}</a>
        </span>
      )
    });

    return (
      <div className="col-md-12 article-list">
        <div className="panel panel-default">
          <div className="panel-heading">
            <h2 className="article-title">
              <a href={title_url}>{article.title}</a>
            </h2>
            <div className="article-meta">
              <ul className="list-inline">
                <li>
                  <a className="" href={author_url}>
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
            <div dangerouslySetInnerHTML={{__html: content}} />
          </div>
          <div className="panel-footer clearfix"></div>
        </div>
      </div>
    );
  }
});
