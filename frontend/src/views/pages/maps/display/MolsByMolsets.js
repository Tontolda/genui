import React from 'react';
import { Card, CardBody } from 'reactstrap';
import { groupByMolset, TabWidget } from '../../../../genui';

function MoleculeDetail(props) {
  const mol = props.mol;

  return (
    <Card>
      <CardBody>{mol.smiles}</CardBody>
    </Card>
  )
}

function MolSetDetail(props) {
  // const molset = props.molset;
  const mols = props.mols;

  return (
    <React.Fragment>
      {
        mols.map(mol => (
          <MoleculeDetail key={mol.id} mol={mol}/>
        ))
      }
    </React.Fragment>
  )

}

export function MolsByMolsetsTabs(props) {
  const groupedMols = props.groupedMols;
  const molsets = props.molsets;
  const mols = props.mols;

  const tabs = [];
  let activeTab = undefined;
  Object.keys(groupedMols).forEach(molsetID => {
    const molset = molsets.find(item => item.id === Number(molsetID));
    const data = groupedMols[molsetID];
    if (!activeTab) {
      activeTab = molset.name;
    }
    tabs.push({
      title: molset.name
      , renderedComponent : props => (
        <MolSetDetail
          {...props}
          molset={molset}
          mols={data.map(item => item.mol)}
          points={data.map(item => item.point)}
        />
      )
    })
  });

  return (
    <div className="genui-map-molsets-grouped">
      {
        mols.length > 0 ? <TabWidget {...props} tabs={tabs} activeTab={activeTab}/> : <p>Select molecules in the map to see details.</p>
      }
    </div>
  )
}

export function MolsByMolsets(props) {
  const mols = props.selectedMols;
  const points = props.selectedPoints;
  const molsets = props.map.molsets;
  const molsGroupedbyMolSet = groupByMolset(mols, molsets, (mol, idx) => {
    return {
      mol: mol,
      point: points[idx]
    }
  });

  const RenderedComponent = props.component;
  return (
    <RenderedComponent
      {...props}
      molsets={molsets}
      mols={mols}
      groupedMols={molsGroupedbyMolSet}
    />
  )
}