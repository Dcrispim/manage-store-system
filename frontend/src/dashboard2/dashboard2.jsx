
import React, { Component } from 'react';
import axios from 'axios'

import ContentHeader from '../common/templates/ContentHeader';
import Content from '../common/templates/Content';
import ValueBox from '../common/widget/ValueBox';
import Row from '../common/layout/Row';

// import { Container } from './styles';

const BASE_URL = 'http://localhost:8000/api'

export default class Dashboard extends Component {
    constructor(props){
        super(props)
        this.state = {credit:0, debt:0}
    }

  componentWillMount(){
    axios.get(`${BASE_URL}/summary/`)
        .then( resp => this.setState(resp.data))
        .catch(err => console.log(err) )
  }

  render() {
    const {credit, debt } = this.state

    return (
        <div>
            <ContentHeader title='Dashboard' small='Versão 2.0'/>
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
