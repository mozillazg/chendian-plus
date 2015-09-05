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
  mixins: [PaginationMixin],

  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var checkinNodes = this.state.data.map(function (checkin) {
      var think = text2html(filterXSS(checkin.think));
      var bookURL = '/b/name/' + checkin.book_name + '/';
      return (
        <Checkin checkin={checkin} key={checkin.id}>
          #打卡 <a href={bookURL}>《{checkin.book_name}》</a>
          <span dangerouslySetInnerHTML={{__html: think}} />
        </Checkin>
      )
    });
    return (
      <div>
        {checkinNodes}
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
