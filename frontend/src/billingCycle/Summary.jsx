import React from 'react'
import Grid from '../common/layout/Grid';
import Row from '../common/layout/Row';
import ValueBox from '../common/widget/ValueBox';
export default ({credits, debts}) => (
        <Grid cols='12'>
            <fieldset>
                <legend>
                    <Row>
                        <ValueBox cols='12 4' color='green' value={credits} 
                            icon='bank' text='Total de Cŕeditos'
                        />
                        <ValueBox cols='12 4' color='red' value={debts} 
                            icon='credit-card' text='Total de Débitos'
                        />
                        <ValueBox cols='12 4' color='blue' value={credits-debts} 
                            icon='money' text='Total Consolidado'
                        />
                    </Row>
                </legend>
            </fieldset>
        </Grid>
    )
