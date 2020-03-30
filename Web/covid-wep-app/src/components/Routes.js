import React from "react"
import { Route, Switch } from "react-router-dom"
import { About, Extension, NotFound } from "./Components"
import App from '../App'

const Routes = () => {
    return (
        <div>
            <Switch>
                <Route exact path="/" component={App} />
                <Route exact path="/About" render={(props) => <About {...props}/>} />
                <Route exact path="/Extension" render={(props) => <Extension {...props}/>} />
                <Route component={NotFound} />
            </Switch>

        </div>
    )
}

export default Routes