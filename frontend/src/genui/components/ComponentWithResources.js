import React from 'react';
import withUnmounted from '@ishawnwang/withunmounted';

class ComponentWithResources extends React.Component {
  abort = new AbortController();
  hasUnmounted = false;

  constructor(props) {
    super(props);

    this.definition = this.props.definition;
    this.updateAfterTasksDone = this.props.updateAfterTasksDone ? this.props.updateAfterTasksDone : false;

    this.state = {
      allLoaded : false,
      data : {}
    }
  }

  componentDidMount() {
    this.updateResources();
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (this.updateAfterTasksDone && prevProps.tasksRunning && !this.props.tasksRunning) {
      this.updateResources();
    }
  }

  updateResources = () => {
    for (let [name, url] of Object.entries(this.definition)) {
      this.fetchResource(name, url);
    }
  };

  componentWillUnmount() {
    this.abort.abort();
  }

  fetchResource = (name, url) => {
    fetch(url, {signal : this.abort.signal})
      .then(response => response.json())
      .then((data) => {
        if (this.hasUnmounted) {
          return
        }

        this.setState((prevState) => {
          prevState.data[name] = data;
          if (Object.keys(prevState.data).length === Object.keys(this.definition).length) {
            prevState.allLoaded = true;
          }
          return prevState;
        });
      })
      .catch(e => console.log(e))
    ;
  };

  render() {
    return this.props.children(this.state.allLoaded, this.state.data);
  }

}

export default withUnmounted(ComponentWithResources);