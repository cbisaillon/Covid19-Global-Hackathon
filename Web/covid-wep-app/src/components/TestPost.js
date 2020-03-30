import React, { Component } from 'react'
import '../App.css';
import { Row, Textarea, Button } from 'react-materialize';
import axios from 'axios';
import { trackPromise } from 'react-promise-tracker';
import { usePromiseTracker } from "react-promise-tracker";
import Loader from 'react-loader-spinner';

export default class TestPost extends Component {

    constructor(props) {
        super(props)
        this.state = { 
            userInput: "",
        }
    }

    render() {

        const LoadingIndicator = props => {
            const { promiseInProgress } = usePromiseTracker({area : props.area});
            
            return (
              promiseInProgress && 
                <div
                style={{
                marginTop: -60,
                marginLeft: 15,
                width: "100%",
                height: "100",
              }}
            >
              <Loader type="ThreeDots" color="royalblue" height='30' width='30' />
            </div>
              );  
             }

        return (
            <div style={{ marginTop: 20 }}>
                <div className="outerBox">
                    <h6 style={{ fontWeight: 500 }}>Test your URL</h6>
                    <Row style={{ marginBotton: 0 }}>
                        <Textarea
                            s={12}
                            className="custom-textArea"
                            placeholder="Please write here..."
                            data-length={120}
                            onChange={(event) => (this.setState({ userInput: event.target.value }))}
                        />
                    </Row>

                    <div style={{ height: "0", display:"flex" }}>
                        <Button
                            small
                            waves="light"
                            style={
                                {
                                    backgroundColor: "royalBlue",
                                    marginTop: -60
                                }
                            }
                            onClick={() => {
                                const config = {
                                    headers: { 'Access-Control-Allow-Origin': '*' }
                                };
                                trackPromise(
                                    axios.get('https://cors-anywhere.herokuapp.com/https://4ua127bd2e.execute-api.us-east-2.amazonaws.com/api/predict-url/?url=' + this.state.userInput, config)
                                        .then(res => {
                                            console.log(res.data)
                                            if(res.data.error){
                                                alert(res.data.error)
                                            }else{
                                                alert("Our algorithm has detected that this article has a " + Math.ceil(res.data.chance*100) + "% chance of being fake")
                                            }
                                        }), 'testing'
                                );
                            }}
                        >
                            Test
                    </Button>
                    <LoadingIndicator area="testing"/>
                    </div>
                </div>
            </div>
        )
    }
}

