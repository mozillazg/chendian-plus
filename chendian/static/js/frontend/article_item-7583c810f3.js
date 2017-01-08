
var Article = React.createClass({displayName: "Article",
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
        React.createElement("span", {key: tag.id, className: ""}, 
          React.createElement("a", {href: url}, tag.name)
        )
      )
    });
    var categories = _categories.map(function (category) {
      var url = "/a/?categories__slug=" + category.slug;
      return (
        React.createElement("span", {key: category.id, className: ""}, 
          React.createElement("a", {href: url}, category.name)
        )
      )
    });

    return (
      React.createElement("div", {className: "col-md-12 article-list"}, 
        React.createElement("div", {className: "panel panel-default"}, 
          React.createElement("div", {className: "panel-heading"}, 
            React.createElement("h2", {className: "article-title"}, 
              React.createElement("a", {href: title_url}, article.title)
            ), 
            React.createElement("div", {className: "article-meta"}, 
              React.createElement("ul", {className: "list-inline"}, 
                React.createElement("li", null, 
                  React.createElement("a", {className: "", href: author_url}, 
                    author.nick_name
                  ), 
                  "于 ", article.created_at, " 发布"
                ), 
                React.createElement("li", null, "tags: ", tags), 
                React.createElement("li", null, "categories: ", categories)
              )
            )
          ), 
          React.createElement("div", {className: "panel-body"}, 
            React.createElement("div", {dangerouslySetInnerHTML: {__html: content}})
          ), 
          React.createElement("div", {className: "panel-footer clearfix"})
        )
      )
    );
  }
});
