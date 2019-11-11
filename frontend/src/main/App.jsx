import React from 'react'
import '../common/templates/dependencies'

import Header from '../common/templates/Header';
import SideBar from '../common/templates/SideBar';
import Footer from '../common/templates/Footer';
import Routes from './routes';
import Messages from '../common/msg/Messages'


export default props => (
    <div className='wrapper'>
        <Header />
        <SideBar />
        <div className="content-wrapper">
            <Routes/>
        </div>
        <Footer/>
        <Messages/>
    </div>
)

