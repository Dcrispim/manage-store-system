import {combineReducers} from 'redux'
import DashboardReducer from '../dashboard/DashboardReducer';
import TabReducers from '../common/tab/TabReducers';
import BillingCyclesReducers from '../billingCycle/BillingCyclesReducers';
import {reducer as formReducer} from 'redux-form'
import {reducer as toastrReducer} from 'react-redux-toastr'



const rootDeducer = combineReducers({
    
    dashboard: DashboardReducer,
    tab: TabReducers,
    billingCycle:BillingCyclesReducers,
    form: formReducer,
    toastr:toastrReducer

})

export default rootDeducer
