import { Card, CardHeader, CardImg } from 'reactstrap';
import React from 'react';
import './compound-list-styles.css'

export function MoleculePic(props) {
  const pic = props.mol.mainPic;
  const As = props.as;

  const { as, ...rest } = props;
  return (
    pic ? <As {...rest} src={pic.image}/> : <p>No image found.</p>
  )
}

export function MoleculeDetail(props) {
  const mol = props.mol;

  return (
    <Card className="compound-list-card">
      <CardHeader>
        <MoleculePic mol={mol} as={CardImg} top width="100%" alt={mol.smiles}/>
      </CardHeader>
    </Card>
  )
}