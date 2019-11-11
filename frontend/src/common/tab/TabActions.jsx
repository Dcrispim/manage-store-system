import RDC from '../../ReducersConst'

export function selectTab(tabId){
    return {
        type: RDC.TAB_SELECTED,
        payload:tabId
    }
}

export function showTabs(...tabIds){
    const tabsToShow = {}
    tabIds.forEach(e => tabsToShow[e] = true)

    return {
        type: RDC.TABS_SHOWED,
        payload: tabsToShow
    }
}