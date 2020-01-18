import React from "react";
import { ResponsiveGrid, TaskAwareComponent } from '../../../genui';
import { Card } from 'reactstrap';
import ModelCard from './ModelCard';
import ModelCardNew from './ModelCardNew';

class ModelGrid extends React.Component {

  render() {
    const models = [];
    const existing_cards = models.map(model => ({
      id : model.id,
      h : {"md" : 9, "sm" : 8},
      w : {"md" : 1, "sm" : 1},
      minH : {"md" : 3, "sm" : 3},
      data : model
    }));
    const new_card = {
      id : "new-mol-set",
      h : {"md" : 7, "sm" : 6},
      w : {"md" : 1, "sm" : 1},
      minH : {"md" : 3, "sm" : 3},
      data : {}
    };

    return (
      <ResponsiveGrid
          items={existing_cards.concat(new_card)}
          rowHeight={75}
          mdCols={2}
          smCols={1}
        >
          {
            existing_cards.map(
              item => (
                <Card key={item.id.toString()}>
                  <TaskAwareComponent
                    handleResponseErrors={this.props.handleResponseErrors}
                    tasksURL={new URL(`models/${item.data.id}/tasks/all/`, this.props.apiUrls.qsarRoot)}
                    render={
                      (taskInfo, onTaskUpdate) => (
                        <ModelCard
                          {...this.props}
                          {...taskInfo}
                          onTaskUpdate={onTaskUpdate}
                          molset={item.data}
                          onModelDelete={this.props.handleModelDelete}
                        />
                      )
                    }
                  />
                </Card>
              )
            ).concat([(
              <Card key={new_card.id} id={new_card.id}>
                <ModelCardNew
                  {...this.props}
                  handleCreateNew={this.props.handleAddModel}/>
              </Card>
            )])
          }
        </ResponsiveGrid>
    )
  }
}

export default ModelGrid