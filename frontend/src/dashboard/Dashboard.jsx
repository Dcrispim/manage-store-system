import React, { Component } from 'react';
import {connect} from 'react-redux'
import {bindActionCreators} from 'redux'

import {getSummary} from './DashboardActions'
import ContentHeader from '../common/templates/ContentHeader';
import Content from '../common/templates/Content';
import ValueBox from '../common/widget/ValueBox';
import Row from '../common/layout/Row';

// import { Container } from './styles';

class Dashboard extends Component {

  componentWillMount(){
    this.props.getSummary()
  }

  render() {
    const {credit, debt } = this.props.summary

    return (
        <div>
            <ContentHeader title='Dashboard' small='Versão 1.0'/>
            <Row>
              <Content>
                  <ValueBox cols='12 4' color='green' icon='bank'
                    value={credit} text='Total de Cŕeditos' />
                  <ValueBox cols='12 4' color='red' icon='credit-card'
                    value={debt} text='Total de Débitos'/>
                  <ValueBox cols='12 4' color='blue' icon='money'
                    value={credit - debt} text='Valor Consolidado'/>
              </Content>
            </Row>
        </div>
        );
  }
}

const mapStateToProps = state => ({
  summary: state.dashboard.summary
});
const mapDispatchToProps = dispatch => bindActionCreators({getSummary}, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Dashboard)

