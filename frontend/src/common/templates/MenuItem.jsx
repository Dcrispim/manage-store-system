import React from 'react';
const MenuItem = (props) => (
    <li>
        <a href={props.path}>
            <i className={`fa fa-${props.icon}`}></i><span> {props.label}</span>
        </a>
    </li>
);

export default MenuItem;