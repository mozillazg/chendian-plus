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
      <div className="member">
        <div className="avatar-120">
          <img data-src="holder.js/120x120/random" className="img-rounded"
            alt="120x120" style={{width: "120px", height: "120px"}}
            title={member.nick_name}/>
        </div>
        <div className="detail">
          <ul className="list-unstyled">
            <li>编号: <span>{member.sn}</span></li>
            <li>昵称: <span>{member.nick_name}</span></li>
            <li>简介: <span><br />{member.note}</span></li>
          </ul>
        </div>
      </div>
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
      var think = checkin.think.replace('\n', '<br>');
      return (
        <Checkin sn={checkin.sn} qq={checkin.qq} nickName={checkin.nick_name}
          date={checkin.posted_at}>
          #打卡 《{checkin.book_name}》{think}
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

