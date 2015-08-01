var ArticleDetail = React.createClass({
  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data, status, xhr) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  getInitialState: function() {
    return {data: {}};
  },

  render: function() {
    return (
      <div>
        <Article article={this.state.data} />
      </div>
    );
  }
});

var id = $("#article-detail").data("id");
var url = '/api/blog/articles/' + id + '/';
React.render(
  <ArticleDetail url={url} />,
  document.getElementById('article-detail')
);
