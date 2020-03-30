import React from "react"
import ReactDOM from "react-dom"
import "./index.css"
import Routes from "./components/Routes"
import { Router } from "react-router-dom"
import createHistory from 'history/createBrowserHistory'
import * as serviceWorker from "./serviceWorker"
const history = createHistory()

ReactDOM.render(
  <Router history={history}>
    <Routes />
  </Router>,
  document.getElementById("root")
)

serviceWorker.unregister()