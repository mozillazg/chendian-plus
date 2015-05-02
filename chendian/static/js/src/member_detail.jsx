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
    var url = '/m/' + member.id;
    var memberInfo = (
      <div className="member">
        <div className="avatar-120 col-md-5">
          <a href={url}>
            <img data-src="holder.js/120x120/random" className="img-rounded"
              alt={member.nick_name} style={{width: "120px", height: "120px"}}
              src={member.avatar} title={member.nick_name} id="member-avatar" />
          </a>
        </div>
        <div className="detail col-md-7">
          <ul className="list-unstyled">
            <li>编号: <span>{member.sn}</span></li>
            <li>昵称: <span className="editable" data-name="nick_name"
                        data-value={member.nick_name} data-type="text"
                      >{member.nick_name}</span></li>
          </ul>
        </div>
      </div>
      );
    return (
      <div className="member-info">
        {memberInfo}
        <div className="description col-md-12">
          <div className="editable" data-name="description"
           data-value={member.description} data-type="textarea">{member.description}</div>
        </div>
      </div>
    );
  }
});

var Checkin = React.createClass({
  render: function() {
    var sn = this.props.sn || '';
    var url = '/m/sn/' + sn.toString();
    return (
      <div className="checkin">
        <div className="checkin-author">
          <a href={url}>【{this.props.sn}】{this.props.nickName}</a>
          <span className="time">{this.props.date}</span>
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
      var think = checkin.think.replace('\n', '<br />');
      return (
        <Checkin sn={checkin.sn} nickName={checkin.nick_name}
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
var initEditable = function() {
  $('.member-info .editable').editable({
    url: memberURL,
    pk: memberID,
    autotext: 'always',
    validate: function(value) {
      if($.trim(value) == '') {
        return 'This field is required';
      }
    }
  });
};
React.render(
  <MemberInfo url={memberURL} />,
  document.getElementById('profile'),
  function() {
    if ($("#profile").data('editable')) {
      initEditable();
    }
  }
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  <CheckinList url={checkinsURL} />,
  document.getElementById('checkin-list')
);
