import React from 'react'
import { Router, Route, Redirect, hashHistory } from 'react-router'

import Dashboard from '../dashboard2/dashboard2'
import BillingCycle from '../billingCycle/BillingCycle'


// import { Container } from './styles';

const Routes = () => (
    <Router history={hashHistory}>
        <Route path="/" component={Dashboard} />
        <Route path="/billingCycles" component={BillingCycle} />
        <Redirect from='*' to='/' />
    </Router>
);

export default Routes;

