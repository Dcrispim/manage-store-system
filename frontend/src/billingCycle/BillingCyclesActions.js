import axios from 'axios'
import RDC from '../ReducersConst'
import {toastr} from 'react-redux-toastr'
import { reset as resetForm, initialize } from "redux-form";
import { showTabs, selectTab } from '../common/tab/TabActions';


const INITIAL_VALUES = {credits:[{}], debts:[{}]
}

const BASE_URL = 'http://localhost:3003/api'

export function getList(){
    const request = axios.get(`${BASE_URL}/billingCycles`)
    return {
        type: RDC.BILLING_CYCLES_FETCHED,
        payload: request
    }
}

export function create(values){
    return submit(values,'post')
    
}

export function remove(values){
    return submit(values,'delete')
    
}
export function showUpdate(billingCycle){
    return showTab(billingCycle,'Update')
}

export function showRemove(billingCycle){
    return showTab(billingCycle,'Delete')

}

function showTab(billingCycle, Tab){
    return [
        init(),
        showTabs(`tab${Tab}`),
        selectTab(`tab${Tab}`),
        initialize('billingCycleForm', billingCycle)
    ]

}



export function update(values){
    return submit(values, 'put')
}

function submit(values, method){
    return dispath => {
        const id = values._id ? values._id : ''
        axios[method](`${BASE_URL}/billingCycles/${id}`, values)
        .then(resp => {
            toastr.success('Sucesso!', 'Operação Realizada com sucesso')
            dispath(init())

        })
        .catch(e => {
            e.response.data.errors.forEach(error => toastr.error('Erro',error))
        })
    }
}




export function init(){
    return [
        showTabs('tabList','tabCreate'),
        selectTab('tabList'),
        getList(),
        initialize('billingCycleForm', INITIAL_VALUES)

    ]
}
