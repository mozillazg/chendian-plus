var Member = React.createClass({
  render: function() {
    var member = this.props.member;
    var url = '/m/' + member.id + '/';
    return (
      <li className="member" data-author="" data-desc={member.note}>
        <a href={url}>
          <img data-src="holder.js/48x48/random" className="img-rounded"
            alt="48x48" style={{width: "48px", height: "48px"}}
            title={member.nick_name}/>
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
        <Member member={member}></Member>
      )
    });
    return (
      <ul className="list-inline member-list">{memberNodes}</ul>
    );
  }
});

React.render(
  <MemberList url='/api/members/' />,
  document.getElementById('member-list')
);

