var PaginationMixin = {
  loadDataFromServer: function() {
    var page = this.state.page || 1;
    var url = this.props.url;
    var search = location.search;
    if (url.indexOf('?') == -1) {
      url = url + search;
    } else if (search.length != 0) {
      url = url + '&' + search.slice(1);
    }
    $.ajax({
      url: url,
      data: {
        'page': page,
        'per_page': this.props.per_page
      },
      dataType: 'json',
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data, status, xhr) {
        var max_page = xhr.getResponseHeader('X-LastPage');
        var total_count = xhr.getResponseHeader('Total-Count');
        this.setState({data: data, max_page: max_page,
                       total_count: total_count, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
        this.setState({data: [], max_page: 0, total_count: 0, loading: false});
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
    location.hash = (this.props.pageKey || '#p') + page;
  },

  handleNextPageClick: function(event) {
    var max_page = this.state.max_page;
    if (max_page == 1) {return};
    var page = this.state.page + 1 || 1;
    if (page > max_page) {
      page = 1;
    }
    location.hash = (this.props.pageKey || '#p') + page;
  },

  getPageNumber: function() {
    return parseInt(location.hash.split(this.props.pageKey || '#p')[1]) || 1;
  },

  getInitialState: function() {
    var page = this.getPageNumber();
    return {data: [], page: page, max_page: 1, route: this.props.route};
  },

  hashchange: function() {
    var page = this.getPageNumber();
    this.setState({page: page}, function() {
      this.loadDataFromServer();
    }.bind(this));
  },

  componentDidMount: function() {
    this.loadDataFromServer();
    window.addEventListener('hashchange', this.hashchange);
  },

  loading: function() {
    return (
      React.createElement("div", {dangerouslySetInnerHTML: {__html: loadingDiv()}})
    )
  },
};
