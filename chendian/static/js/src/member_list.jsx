var Member = React.createClass({
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      <li className="member" data-author="" data-desc={member.note}>
        <a href={url}>
          <img data-src="holder.js/48x48/random" className="img-rounded"
            alt={member.nick_name} style={{width: "48px", height: "48px"}}
            src={member.avatar} title={member.nick_name}/>
        </a>
      </li>
    );
  }
});

var MemberList = React.createClass({
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
        <Member member={member} key={member.id}></Member>
      )
    });
    return (
      <ul className="list-inline member-list">{memberNodes}</ul>
    );
  }
});

React.render(
  <MemberList url='/api/members/?per_page=1000' />,
  document.getElementById('member-list')
);

