import axios from 'axios'
import { BILLING_SUMMARY_FATCHED } from "../ReducersConst";

const BASE_URL = 'http://localhost:3003/api'

export function getSummary(){
    const request = axios.get(`${BASE_URL}/billingCycles/summary`)
    return{
        type: BILLING_SUMMARY_FATCHED ,
        payload: request
    }
}