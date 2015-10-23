var ArticleDetail = React.createClass({
  loadDataFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data) {
        this.setState({data: data, loading: false});
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

  loading: function() {
    return (
      <div dangerouslySetInnerHTML={{__html: loadingDiv()}} />
    )
  },
  render: function() {
    if (this.state.loading) {
      return this.loading();
    }
    return (
      <div>
        <Article article={this.state.data} />
      </div>
    );
  }
});

var id = $("#article-detail").data("id");
var url = '/api/blog/articles/' + id + '/';
ReactDOM.render(
  <ArticleDetail url={url} />,
  document.getElementById('article-detail')
);
