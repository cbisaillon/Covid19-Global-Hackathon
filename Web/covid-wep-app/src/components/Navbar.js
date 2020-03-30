import React from 'react'
import { Navbar, Icon, NavItem, Container } from 'react-materialize';
import '../App.css';

export default () => {

    const navBarBackgroundStyle = {
        background: "royalblue",
    }

    return (
        <div style={navBarBackgroundStyle}>
            <Container>
                <Navbar
                    style={{color:"white"}}
                    className="custom-navbar"
                    alignLinks="right"
                    brand={
                        <a
                            className="brand-logo"
                            href="/"
                            style={{ paddingTop: "auto", textDecoration: "none" }}
                        >
                            Fakebook
                        </a>
                    }
                    menuIcon={<Icon>menu</Icon>}
                    options={{
                        draggable: true,
                        edge: 'left',
                        inDuration: 250,
                        onCloseEnd: null,
                        onCloseStart: null,
                        onOpenEnd: null,
                        onOpenStart: null,
                        outDuration: 200,
                        preventScrolling: true
                    }}
                >
                    <NavItem href='/About' style={{textDecoration:"none"}}>
                        About
                    </NavItem>
                    <NavItem href='/Extension' style={{textDecoration:"none"}}>
                        Extension
                    </NavItem>
                </Navbar>
            </Container>
        </div>


    )
}
