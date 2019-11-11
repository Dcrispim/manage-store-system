import React, { Component } from 'react';
import {bindActionCreators} from 'redux'
import {connect} from 'react-redux'

import Content from "../common/templates/Content";
import ContentHeader from "../common/templates/ContentHeader";
import Tabs from '../common/tab/Tabs';
import TabsContent from '../common/tab/TabsContent';
import TabsHeader from '../common/tab/TabsHeader';
import TabHeader from '../common/tab/TabHeader';
import TabContent from '../common/tab/TabContent';
import { init, create, update, remove } from "../billingCycle/BillingCyclesActions";

import BillingCyclesList from './BillingCyclesList';
import BillingCyclesForm from './BillingCyclesForm';




class BillingCycle extends Component {
  componentDidMount(){
    this.props.init()
  }

  render() {
    return (
    <div>
        <ContentHeader title='Ciclos de Pagamento' small='Cadastro' />
        <Content>
            <Tabs>
               <TabsHeader>
                  <TabHeader label='Listar' icon='bars' target='tabList' />
                  <TabHeader label='Incluir' icon='plus' target='tabCreate' />
                  <TabHeader label='Alterar' icon='pencil' target='tabUpdate' />
                  <TabHeader label='Excluir' icon='trash-o' target='tabDelete' />

               </TabsHeader>
               <TabsContent>
                  <TabContent id='tabList'>
                    <BillingCyclesList/>
                  </TabContent>
                  <TabContent id='tabCreate'>
                    <BillingCyclesForm onSubmit={this.props.create} btn='primary' text='Incluir'/>
                  </TabContent>
                  <TabContent id='tabUpdate'>
                    <BillingCyclesForm onSubmit={this.props.update} btn='warning' text='Alterar'/>
                  </TabContent>
                  <TabContent id='tabDelete'>
                  <BillingCyclesForm onSubmit={this.props.remove} btn='danger' text='Delete' readOnly={true}/>
                  </TabContent>

               </TabsContent>
            </Tabs>
        </Content>
    </div>

        );
  }
}

const mapDispatchToProps = dispatch =>
  bindActionCreators({init,create, update, remove}, dispatch);
export default connect(null, mapDispatchToProps)(BillingCycle)