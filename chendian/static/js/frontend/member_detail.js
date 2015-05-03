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
    var url = '/m/' + member.id;
    var memberInfo = (
      React.createElement("div", {className: "member"}, 
        React.createElement("div", {className: "avatar-120 col-md-5"}, 
          React.createElement("a", {href: url}, 
            React.createElement("img", {"data-src": "holder.js/120x120/random", className: "img-rounded", 
              alt: member.nick_name, style: {width: "120px", height: "120px"}, 
              src: member.avatar, title: member.nick_name, id: "member-avatar"})
          )
        ), 
        React.createElement("div", {className: "detail col-md-7"}, 
          React.createElement("ul", {className: "list-unstyled"}, 
            React.createElement("li", null, "编号: ", React.createElement("span", null, member.sn)), 
            React.createElement("li", null, "昵称: ", React.createElement("span", {className: "editable", "data-name": "nick_name", 
                        "data-value": member.nick_name, "data-type": "text"
                      }, member.nick_name))
          )
        )
      )
      );
    return (
      React.createElement("div", {className: "member-info"}, 
        memberInfo, 
        React.createElement("div", {className: "description col-md-12"}, 
          React.createElement("div", {className: "editable", "data-name": "description", 
           "data-value": member.description, "data-type": "textarea"}, member.description)
        )
      )
    );
  }
});

var Checkin = React.createClass({displayName: "Checkin",
  render: function() {
    var checkin = this.props.checkin;
    var sn = checkin.sn || '';
    var url = '/m/sn/' + sn.toString();
    return (
      React.createElement("div", {className: "checkin"}, 
        React.createElement("div", {className: "checkin-author"}, 
          React.createElement("a", {href: url}, "【", sn, "】", checkin.nick_name), 
          React.createElement("span", {className: "time"}, checkin.posted_at)
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
      var think = checkin.think.replace('\n', '<br />');
      var bookURL = '/b/name/' + checkin.book_name;
      return (
        React.createElement(Checkin, {checkin: checkin, key: checkin.id}, 
          "#打卡 ", React.createElement("a", {href: bookURL}, "《", checkin.book_name, "》"), " ", think
        )
      )
    });
    return (React.createElement("div", null, checkinNodes));
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
  React.createElement(MemberInfo, {url: memberURL}),
  document.getElementById('profile'),
  function() {
    if ($("#profile").data('editable')) {
      initEditable();
    }
  }
);

var checkinsURL = memberURL + 'checkins/';
React.render(
  React.createElement(CheckinList, {url: checkinsURL}),
  document.getElementById('checkin-list')
);
