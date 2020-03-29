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
                    className="custom-navbar"
                    alignLinks="right"
                    brand={
                        <a
                            className="brand-logo"
                            href=""
                            style={{ paddingTop: "auto" }}
                        >
                            {/*<img src={Fb} alt="logo" height="40px" />*/}
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
                    <NavItem>
                        Search
                    </NavItem>
                    <NavItem>
                        About
                    </NavItem>
                    <NavItem>
                        Extension
                    </NavItem>
                </Navbar>
            </Container>
        </div>


    )
}
