import React from 'react';
import * as Yup from 'yup';

class ModelFormRenderer extends React.Component {
  CTYPE_TO_VALIDATOR = {
    string: Yup.string().required(),
    integer: Yup.number().required(),
    float: Yup.number().required(),
    bool: Yup.bool().required()
  };

  constructor(props) {
    super(props);

    this.chosenAlgorithm = this.props.chosenAlgorithm;
    this.modes = this.props.chosenAlgorithm.validModes;
    this.parameters = !this.props.omitAlgParams ? this.props.chosenAlgorithm.parameters : null;
    this.metrics = !this.props.omitValidation ? this.props.metrics : null;
    this.enableFileUploads = this.props.enableFileUploads;
    this.disabledModelFormFields = this.props.disabledModelFormFields ? this.props.disabledModelFormFields : [];
    this.initialValues = this.generateInit();
    this.schema = this.generateSchema();
  }

  generateInit = () => {
    const trainingStrategyDefaultInit = {
      algorithm: this.chosenAlgorithm.id,
      mode: this.modes[0].id,
    };
    const trainingStrategyInit = Object.assign(trainingStrategyDefaultInit, this.props.trainingStrategyInit ? this.props.trainingStrategyInit : {});
    const validationStrategyDefaultInit = this.metrics && !this.disabledModelFormFields.includes('validationStrategy.metrics') ? {
      metrics: [this.metrics[0].id]
    } : {};
    const validationStrategyInit = Object.assign(validationStrategyDefaultInit, this.props.validationStrategyInit ? this.props.validationStrategyInit : {});

    let initialValues = {
      name: `New ${this.chosenAlgorithm.name} Model`,
      description: '',
      project: this.props.project.id,
      trainingStrategy: trainingStrategyInit
    };
    if (this.enableFileUploads) {
      initialValues.modelFile = undefined;
    }

    // validation
    if (Object.keys(validationStrategyInit).length !== 0 && validationStrategyInit.constructor === Object) {
      initialValues.validationStrategy = validationStrategyInit;
    }

    // extra parameters
    initialValues = Object.assign(initialValues, this.props.extraParamsInit ? this.props.extraParamsInit : {});

    // default parameters
    if (this.parameters) {
      const parameterDefaults = {};
      for (const param of this.parameters) {
        parameterDefaults[param.name] = param.defaultValue;
      }
      initialValues.trainingStrategy.parameters = parameterDefaults;
    }

    // console.log(initialValues);

    return initialValues;
  };

  generateSchema = () => {
    const trainingStrategyDefault = {
      algorithm: Yup.number().integer().positive("Algorithm ID needs to be a positive number").required('Algorithm ID must be supplied'),
      mode: Yup.number().integer()
        .max(256, 'Mode must be 256 characters or less.').required('You must specify a mode.'),
    };

    // parameters
    if (this.parameters) {
      const parameterValidators = {};
      for (const param of this.parameters) {
        parameterValidators[param.name] = this.CTYPE_TO_VALIDATOR[param.contentType]
      }
      trainingStrategyDefault.parameters = Yup.object().shape(parameterValidators);
    }

    const trainingStrategy = Object.assign(trainingStrategyDefault, this.props.trainingStrategySchema);
    // the main schema object
    let validationObj = {
      name: Yup.string()
        .max(256, 'Name must be less than 256 characters long.')
        .required('Name is required.'),
      description: Yup.string()
        .max(10000, 'Description must be 10,000 characters or less.'),
      project: Yup.number().integer().positive("Project ID needs to be a positive number").required('Project ID must be supplied'),
      trainingStrategy: Yup.object().shape(
        trainingStrategy
      )
    };
    if (this.enableFileUploads) {
      validationObj.modelFile = Yup.mixed().required("Model file is required.");
    }

    // validation added only if there is something to add
    const validationStrategyDefault = this.metrics && !this.disabledModelFormFields.includes('validationStrategy.metrics') ? {
      metrics: Yup.array().of(Yup.number().positive('Metric ID must be a positive integer.')).required('You need to supply one or more validation metrics for validation.'),
    } : {};
    const validationStrategy = Object.assign(validationStrategyDefault, this.props.validationStrategySchema);
    if (Object.keys(validationStrategy).length !== 0 && validationStrategy.constructor === Object) {
      validationObj.validationStrategy = Yup.object().shape(
        validationStrategy
      );
    }

    // extra parameters
    validationObj = Object.assign(validationObj, this.props.extraParamsSchema);

    // console.log(validationObj);
    return Yup.object().shape(validationObj);
  };

  render() {
    const FormComponent = this.props.component;

    return (
      <FormComponent
        {...this.props}
        initialValues={this.initialValues}
        validationSchema={this.schema}
        modes={this.modes}
        parameters={this.parameters}
      />
    );
  }
}

export default ModelFormRenderer;