import React from 'react'

export default props => (
    <button type={`${props.type ? props.type: 'button'}`} className={`btn btn-${props.btn}`} onClick={props.onClick}>
        <i className={`fa fa-${props.icon}`}/>
    </button>
)
