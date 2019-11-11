import React from 'react';

// import { Container } from './styles';

const ContentHeader = (props) =>(
    
    <section className="content-header">

        <h1>{props.title}<small>{props.small}</small></h1>

    </section>

    );

export default ContentHeader;

