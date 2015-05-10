var PaginationMixin = {
  loadDataFromServer: function() {
    var page = this.state.page || 1;
    $.ajax({
      url: this.props.url,
      data: {
        'page': page,
        'per_page': this.props.per_page
      },
      dataType: 'json',
      success: function(data, status, xhr) {
        var max_page = xhr.getResponseHeader('X-LastPage');
        this.setState({data: data, max_page: max_page});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handlePerPageClick: function(event) {
    var max_page = this.state.max_page;
    if (max_page == 1) {return};
    var page = this.state.page - 1;
    if (page == 0) {
      page = max_page;
    }
    this.setState({page: page}, function() {
        location.hash = ('#p' + page);
        this.loadDataFromServer();
    }.bind(this));
  },

  handleNextPageClick: function(event) {
    var max_page = this.state.max_page;
    if (max_page == 1) {return};
    var page = this.state.page + 1 || 1;
    if (page > max_page) {
      page = 1;
    }
    this.setState({page: page}, function() {
        location.hash = ('#p' + page);
        this.loadDataFromServer();
    }.bind(this));
  },

  getInitialState: function() {
    var page = parseInt(location.hash.split('#p')[1]) || 1;
    return {data: [], page: page, max_page: 1};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },
};
