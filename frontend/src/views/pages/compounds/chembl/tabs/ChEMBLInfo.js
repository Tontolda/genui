import React from 'react';
import { Col, Row } from 'reactstrap';
import MolSetTasks from './MolSetTasks';

class MolsStats extends React.Component {
  // TODO: convert this class to use the LiveObject

  constructor(props) {
    super(props);

    this.state = {
      molCount : 0,
      lastUpdate : null
    }
  }

  componentDidMount() {
    this.fetchUpdates();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    const time_now = new Date().getTime();
    if (!prevState.lastUpdate || (time_now - prevState.lastUpdate > 2000)) {
      this.fetchUpdates();
    }
  }

  fetchUpdates = () => {
    // FIXME: this also causes a no-op so make sure to clear the fetch request on unmount
    // TODO: add proper request error handling
    fetch(this.props.moleculesURL)
      .then(response => response.json())
      .then(this.updateMolStats)
  };

  updateMolStats = (data) => {
    // TODO: fetch more data about compounds to show
    this.setState({
      molCount : data.count
      , lastUpdate : new Date().getTime()
    });
  };

  render() {
    return (
      <React.Fragment>
        <h4>Compounds</h4>
        <p>Unique in Total: {this.state.molCount}</p>
        <h4>Associated Targets</h4>
        <ul>
          {
            this.props.molset.targets.map(
              target => <li key={target.targetID}>{target.targetID}</li>
            )
          }
        </ul>
      </React.Fragment>
    )
  }
}

class ChEMBLInfo extends React.Component {

  constructor(props) {
    super(props);

    this.molset = this.props.molset;
  }

  render() {
    return (
      <Row>
        <Col sm="12">
          <h4>Description</h4>
          <p>{this.molset.description}</p>
          <MolsStats
            molset={this.props.molset}
            moleculesURL={this.props.moleculesURL}
            molsetIsUpdating={this.props.molsetIsUpdating}
          />
          <MolSetTasks
            progressURL={this.props.apiUrls.celeryProgress}
            tasks={this.props.tasks}
            molset={this.props.molset}
          />
        </Col>
      </Row>
    );
  }
}

export default ChEMBLInfo;