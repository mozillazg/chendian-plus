var MemberInfo = React.createClass({displayName: "MemberInfo",
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
      React.createElement("div", {className: "member"}, 
        React.createElement("div", {className: "avatar-120"}, 
          React.createElement("img", {"data-src": "holder.js/120x120/random", className: "img-rounded", 
            alt: "120x120", style: {width: "120px", height: "120px"}, 
            title: member.nick_name})
        ), 
        React.createElement("div", {className: "detail"}, 
          React.createElement("ul", {className: "list-unstyled"}, 
            React.createElement("li", null, "编号: ", React.createElement("span", null, member.sn)), 
            React.createElement("li", null, "昵称: ", React.createElement("span", null, member.nick_name)), 
            React.createElement("li", null, "简介: ", React.createElement("span", null, React.createElement("br", null), member.note))
          )
        )
      )
      );
    return (
      React.createElement("div", {className: "member-info"}, 
        memberInfo
      )
    );
  }
});

var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          "【", this.props.sn, "】", this.props.nickName, "(", this.props.qq, ") ", this.props.date
        ), 
        React.createElement("div", {className: "checkin-content"}, 
          this.props.children
        )
      )
    );
  }
});

var CheckinList = React.createClass({displayName: "CheckinList",
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
        React.createElement(Checkin, {sn: checkin.sn, qq: checkin.qq, nickName: checkin.nick_name, 
          date: checkin.posted_at}, 
          "#打卡 《", checkin.book_name, "》", checkin.think
        )
      )
    });
    return (React.createElement("div", null, checkinNodes));
  }
});

var memberID = $('#profile').data('id');
var memberURL = '/api/members/' + memberID + '/';
React.render(
  React.createElement(MemberInfo, {url: memberURL}),
  document.getElementById('profile')
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  React.createElement(CheckinList, {url: checkinsURL}),
  document.getElementById('checkin-list')
);

