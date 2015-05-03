var Member = React.createClass({displayName: "Member",
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      React.createElement("li", {className: "member", "data-author": "", "data-desc": member.note}, 
        React.createElement("a", {href: url}, 
          React.createElement("img", {className: "img-rounded", 
            alt: member.nick_name, style: {width: "48px", height: "48px"}, 
            src: member.avatar, title: member.nick_name})
        )
      )
    );
  }
});

var MemberList = React.createClass({displayName: "MemberList",
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
    var memberNodes = this.state.data.map(function (member) {
      return (
        React.createElement(Member, {member: member, key: member.id})
      )
    });
    return (
      React.createElement("ul", {className: "list-inline member-list"}, memberNodes)
    );
  }
});

React.render(
  React.createElement(MemberList, {url: "/api/members/?per_page=1000"}),
  document.getElementById('member-list')
);

