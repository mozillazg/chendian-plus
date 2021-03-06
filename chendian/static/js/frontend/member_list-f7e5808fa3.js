
var Member = React.createClass({displayName: "Member",
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      React.createElement("li", {className: "member", "data-author": "", "data-desc": member.note}, 
        React.createElement("a", {href: url}, 
          React.createElement("img", {className: "img-rounded avatar-64 lazyload", 
            alt: member.nick_name, 
            src: member.avatar, "data-src": member.avatar, 
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
      beforeSend: function() {
        this.setState({loading: true});
        return true;
      }.bind(this),
      success: function(data) {
        this.setState({data: data, loading: false});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  loading: function() {
    return (
      React.createElement("div", {dangerouslySetInnerHTML: {__html: loadingDiv()}})
    )
  },
  render: function() {
    if (this.state.loading) {
      return this.loading();
    }

    var memberNodes = this.state.data.map(function (member) {
      return (
        React.createElement(Member, {member: member, key: member.id})
      )
    });
    return (
      React.createElement("div", {ref: "list"}, 
        React.createElement("ul", {className: "list-inline member-list"}, memberNodes)
      )
    );
  }
});

ReactDOM.render(
  React.createElement(MemberList, {url: "/api/members/?per_page=1000&_fields=id,nick_name,avatar"}),
  document.getElementById('member-list')
);
