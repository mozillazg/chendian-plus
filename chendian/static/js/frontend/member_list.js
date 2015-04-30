var Member = React.createClass({displayName: "Member",
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      React.createElement("li", {className: "member", "data-author": "", "data-desc": member.note}, 
        React.createElement("a", {href: url}, 
          React.createElement("img", {"data-src": "holder.js/48x48/random", className: "img-rounded", 
            alt: "48x48", style: {width: "48px", height: "48px"}, 
            title: member.nick_name})
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
        React.createElement(Member, {member: member})
      )
    });
    return (
      React.createElement("ul", {className: "list-inline member-list"}, memberNodes)
    );
  }
});

React.render(
  React.createElement(MemberList, {url: "/api/members/"}),
  document.getElementById('member-list')
);

