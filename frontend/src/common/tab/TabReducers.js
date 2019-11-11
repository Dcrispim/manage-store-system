import RDC from '../../ReducersConst'



const INITIAL_STATE = {selected:'', visible:{}}

export default (state= INITIAL_STATE, action) => {
    switch(action.type){
        case RDC.TAB_SELECTED:
            return {...state, selected: action.payload}

        case RDC.TABS_SHOWED:
            return {...state, visible: action.payload}
        default:
            return state
    }
}
