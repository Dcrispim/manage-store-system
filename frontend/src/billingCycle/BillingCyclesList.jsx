import React, { Component } from 'react';
import { bindActionCreators } from 'redux';
import { connect } from "react-redux";

import { getList, showUpdate, showRemove } from "./BillingCyclesActions";
import IconButton from '../common/layout/IconButton';


class BillingCyclesList extends Component {

    componentWillMount(){
        this.props.getList()
        
    }
    renderRows(){
        const list =  this.props.list || []
        return list.map(bc =>(
            <tr key={bc._id}>
                <td>{bc.nome}</td>
                <td>{bc.month}</td>
                <td>{bc.year}</td>
                <td className='table-actions'>
                    <IconButton btn='warning' icon='pencil' onClick={() => this.props.showUpdate(bc)}/>
                    <IconButton btn='danger' icon='trash-o' onClick={() => this.props.showRemove(bc)}/>
                </td>
            </tr>
        ))
    }

    render() {
        console.log(this.props.list)
        return (
            <div>
                <table className="table">
                    <thead>
                        <tr>
                            <th>Nome</th>
                            <th>Mês</th>
                            <th>Ano</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.renderRows()}
                    </tbody>
                </table>
            </div>
        );
    }
}
const mapStateToProps = state => ({
  list: state.billingCycle.list
});
const mapDispatchToProps = dispatch =>
  bindActionCreators({getList, showUpdate, showRemove }, dispatch);
export default connect(mapStateToProps, mapDispatchToProps)(BillingCyclesList)