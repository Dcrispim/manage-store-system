import React, { Component } from 'react';
import { bindActionCreators } from "redux";
import { connect } from "react-redux";

import { Field, arrayInsert, arrayRemove } from 'redux-form'

import Grid from '../common/layout/Grid';
import Input from '../common/form/Input';
import IconButton from '../common/layout/IconButton';
import If from '../common/operator/If';


class ItemList extends Component {
    add(index, item = {}){
        if(!this.props.readOnly){
            this.props.arrayInsert('billingCycleForm', this.props.field, index, item)
        }
    }
    remove(index){
        if(!this.props.readOnly && this.props.list.length > 1){
            this.props.arrayRemove('billingCycleForm', this.props.field, index)
        }
    }

    renderRows(){
        const list = this.props.list || []
        return  list.map((item, index) => (       
                <tr key={index}>
                    <td><Field name={`${this.props.field}[${index}].nome`}  component={Input}
                    placeholder='informe o nome'
                    readOnly={this.props.readOnly}></Field></td>
                    
                    <td><Field name={`${this.props.field}[${index}].value`} component={Input}
                    placeholder='informe o valor'
                    readOnly={this.props.readOnly}></Field></td>

                    <If test={this.props.status}>
                        <td><Field name={`${this.props.field}[${index}].status`} component={Input}
                        placeholder='informe o status'
                        readOnly={this.props.readOnly}></Field></td>
                    </If>
                    
                    <td>
                        <IconButton icon='plus' btn='success'
                        onClick={() => this.add(index + 1)} />

                        <IconButton icon='clone' btn='warning'
                        onClick={() => this.add(index + 1, item)}/>

                        <IconButton icon='trash-o' btn='danger'
                        onClick={() => this.remove(index)}/>
                    </td>
                </tr>
            )
            
        )
    }
    render() {
        return (
            <Grid cols = {this.props.cols}>

            
                <fieldset>
                        <legend>{this.props.legend}</legend>
                    
                    <table className="table">
                        <thead>
                            <tr>
                            <th>Nome</th>
                            <th>Valor</th>
                            <If test={this.props.status}>
                                <th>Status</th>
                            </If>
                            <th className='table-actions'>Ações</th>
                            </tr>
                        </thead>
                        <tbody>
                            {this.renderRows()}
                        </tbody>
                    </table>
                </fieldset>
            </Grid>
        );
    }
}

const mapDispatchToProps = dispatch =>
  bindActionCreators({arrayInsert, arrayRemove}, dispatch);

export default connect(null, mapDispatchToProps)(ItemList)
