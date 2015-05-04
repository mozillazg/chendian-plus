var Checkin = React.createClass({
  render: function() {
    var checkin = this.props.checkin;
    var sn = checkin.sn || '';
    var url = '/m/sn/' + sn.toString() + '/';
    return (
      <div className="checkin">
        <div className="checkin-author">
          <a href={url}>【{sn}】{checkin.nick_name}</a>
          <span className="time">{checkin.posted_at}</span>
        </div>
        <div className="checkin-content">
          {this.props.children}
        </div>
      </div>
    );
  }
});

var CheckinList = React.createClass({
  loadDataFromServer: function() {
    var page = this.state.page || 1;
    $.ajax({
      url: this.props.url,
      data: {
        'page': page,
        'per_page': this.props.per_page
      },
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },

  handlePerPageClick: function(event) {
    var page = this.state.page - 1 || 1;
    this.setState({page: page}, function() {
        this.loadDataFromServer();
    }.bind(this));
  },

  handleNextPageClick: function(event) {
    var page = this.state.page + 1 || 1;
    this.setState({page: page}, function() {
        this.loadDataFromServer();
    }.bind(this));
  },

  getInitialState: function() {
    return {data: [], page: 1};
  },

  componentDidMount: function() {
    this.loadDataFromServer();
  },

  render: function() {
    var checkinNodes = this.state.data.map(function (checkin) {
      var think = checkin.think.replace('\n', '<br />');
      var bookURL = '/b/name/' + checkin.book_name + '/';
      return (
        <Checkin checkin={checkin} key={checkin.id}>
          #打卡 <a href={bookURL}>《{checkin.book_name}》</a> {think}
        </Checkin>
      )
    });
    return (
      <div>
        {checkinNodes}
        <nav>
          <ul className="pager">
            <li className="previous"><a href="#" onClick={this.handlePerPageClick}>
                <span aria-hidden="true">&larr;</span> Previous</a></li>
            <li><span className="text-center">第 {this.state.page} 页</span></li>
            <li className="next"><a href="#" onClick={this.handleNextPageClick}>
                Next <span aria-hidden="true">&rarr;</span></a></li>
          </ul>
        </nav>
      </div>
    );
  }
});
