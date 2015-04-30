var MemberInfo = React.createClass({
  getInitialState: function() {
    return {data: {}};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var member = this.state.data;
    var memberInfo = (
      <dl className="dl-horizontal">
        <dt>编号</dt>
        <dd>{member.sn}</dd>
        <dt>昵称</dt>
        <dd>{member.nick_name}</dd>
        <dt>简介</dt>
        <dd>{member.note}</dd>
      </dl>
      );
    return (
      <div className="member-info">
        {memberInfo}
      </div>
    );
  }
});

var Checkin = React.createClass({
  render: function() {
    return (
      <div className="checkin">
        <div className="checkin-author">
          【{this.props.sn}】{this.props.nickName}({this.props.qq}) {this.props.date}
        </div>
        <div className="checkin-content">
          {this.props.children}
        </div>
      </div>
    );
  }
});

var CheckinList = React.createClass({
  getInitialState: function() {
    return {data: []};
  },
  componentDidMount: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      success: function(data) {
        this.setState({data: data});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  render: function() {
    var checkinNodes = this.state.data.map(function (checkin) {
      return (
        <Checkin sn={checkin.sn} qq={checkin.qq} nickName={checkin.nick_name}
          date={checkin.posted_at}>
          #打卡 《{checkin.book_name}》{checkin.think}
        </Checkin>
      )
    });
    return (<div>{checkinNodes}</div>);
  }
});

var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';
React.render(
  <MemberInfo url={memberURL} />,
  document.getElementById('profile')
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  <CheckinList url={checkinsURL} />,
  document.getElementById('checkin-list')
);

