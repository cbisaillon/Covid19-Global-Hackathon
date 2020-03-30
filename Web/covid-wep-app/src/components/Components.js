import React from "react"
import { Row, Button } from 'react-materialize';

function textSpace(title, text) {
    return (
        <div style={{ marginTop: 20, marginBottom: 20 }}>
            <div className="outerBox">
                <h1 style={{ fontWeight: 500, textAlign: "center", color: "royalblue" }}>{title}</h1>
                <Row style={{ margin: 30, textAlign:"center" }}>
                    <h4>{text}</h4>
                </Row>
            </div>
        </div>
    )
}


const About = (props) => {

    const aboutText = "The COVID-19 Global Hackathon is an opportunity for developers to build software solutions that drive social impact, with the aim of tackling some of the challenges related to the current coronavirus (COVID-19) pandemic. We’re encouraging YOU - innovators around the world - to #BuildforCOVID19 using technologies of your choice across a range of suggested themes and challenge areas - some of which have been sourced through health partners including the World Health Organization and scientists at the Chan Zuckerberg Biohub. The hackathon welcomes locally and globally focused solutions, and is open to all developers - with support from technology companies and platforms including AWS, Facebook, Giphy, Microsoft, Pinterest, Salesforce, Slack, TikTok, Twitter and WeChat, who will be sharing resources to support participants throughout the submission period."
    const ourMission = "With the World Health Organization (WHO) declaring coronavirus (COVID-19) a global pandemic, governments have issued guidance for members of the community to practice social distancing, while companies have enforced work from home policies in an effort to flatten the curve of viral infections across the population. Given the isolation currently being experienced within communities right now, we want to create an online space where developers can ideate, experiment and build software solutions to help address this crisis.\n\nOur goal is to provide users with a tool to identify fake news and misinformation. Since the beginning of the outbreak, we have seen a surge in false or inaccurate information, especially that which is deliberately intended to deceive on numerous social media. It is our mission to combat fake news and protect the vulnerable."

    return (<div>
        {textSpace("About this Hackathon", aboutText)}
        {textSpace("Our Mission", ourMission)}

        <Button
            small
            waves="light"
            style={
                {
                    backgroundColor: "royalBlue",
                    width: "20%",
                    marginTop: 20,
                    marginLeft: "40%",
                    marginBottom:40
                }
            }
            onClick={
                ()=>{
                    props.history.goBack()
                }
            }
        >
            Back
                    </Button>


    </div>)
}

const Extension = (props) => {

    const extensionText = "Sorry! Unfortunately, due to the Chrome Web store's long approval time, our Chrome Extension has not been approved in by the Chrome Web Store yet... \nWe will update the link as soon as possible!\n Please Stay tuned!"

    return (
        <div>
            {textSpace("Our Chrome Extension", extensionText)}
            <Button
            small
            waves="light"
            style={
                {
                    backgroundColor: "royalBlue",
                    width: "20%",
                    marginTop: 20,
                    marginLeft: "40%",
                    marginBottom:40
                }
            }
            onClick={
                ()=>{
                    props.history.goBack()
                }
            }
        >
            Back
                    </Button>
        </div>
    )
}

const NotFound = () => {
    return "Page not found."
}

export { About, Extension, NotFound }