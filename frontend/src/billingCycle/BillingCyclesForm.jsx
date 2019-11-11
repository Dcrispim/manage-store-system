import React, { Component } from 'react';
import { reduxForm, Field, formValueSelector } from 'redux-form'
import { bindActionCreators } from "redux";
import { connect } from "react-redux";


import LabelAndInput from '../common/form/LabelAndInput'
import { init } from './BillingCyclesActions';
import ItemList from './ItemList';
import Summary from './Summary';



class BillingCyclesForm extends Component {

    calculateSummary(){
        const sum = (t, v) => t+v
        return {
            sumOfCredits: this.props.credits.map(c => +c.value || 0).reduce(sum),
            sumOfDebts: this.props.debts.map(d => +d.value || 0).reduce(sum)
        }
    }

    render() {
        const {handleSubmit, readOnly, credits, debts} = this.props
        const {sumOfCredits, sumOfDebts} = this.calculateSummary()
        return (
            <form role="form" onSubmit={handleSubmit}>
                <div className='box-body'>
                    <Field name='nome' component={LabelAndInput} readOnly={readOnly}
                    label='Nome' cols='12 4' placeholder='Informe o Nome'/>
                    <Field name='month' component={LabelAndInput} readOnly={readOnly}
                    label='Mês' cols='12 4' placeholder='Informe o mês' type='number' />
                    <Field name='year' component={LabelAndInput} readOnly={readOnly}
                    label='Ano' cols='12 4' placeholder='Informe o Ano' type='number' />

                    <Summary credits={sumOfCredits} debts={sumOfDebts}/>

                    <ItemList cols='12 6' list={credits} readOnly={readOnly}
                    field='credits' legend='Créditos' />
                    <ItemList cols='12 6' list={debts} readOnly={readOnly}
                    field='debts' legend='Débitos' status />
                </div>
                <div className="box-footer">
                    <button type='submit' className={`btn btn-${this.props.btn}`}>{this.props.text}</button>
                    <button type='button' onClick={this.props.init} className="btn btn-default">Cancelar</button>
                </div>
            </form>

        );
    }
}

BillingCyclesForm = reduxForm({form: 'billingCycleForm', destroyOnUnmount:false})(BillingCyclesForm)
const selector = formValueSelector('billingCycleForm')

const mapStateToProps = state => ({
    credits: selector(state, 'credits'),
    debts: selector(state, 'debts')
});

const mapDispatchToProps = dispatch =>
  bindActionCreators({init}, dispatch);

export default connect(mapStateToProps,mapDispatchToProps)(BillingCyclesForm)
