import React from 'react'
import { Dropdown, DropdownButton } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faThumbsUp, faThumbsDown } from '@fortawesome/free-solid-svg-icons';
import ReadMoreAndLess from 'react-read-more-less';
import Popup from "reactjs-popup";
import '../App.css';

export default (props) => {

    const postStyle = {
        marginTop: "25px"
    }

    return (
        <div style={postStyle}>
            <div className="outerBox m10">
                <div>
                    <div>
                        <div style={{ display: "flex", marginBottom: 10 }}>
                            <div
                                style={{
                                    width: 40,
                                    height: 40,
                                    borderRadius: 30,
                                    overflow: "hidden"
                                }}
                            >
                                <img
                                    src={props.Picture}
                                    alt="profile photo"
                                    height="100%"
                                />
                            </div>

                            <div style={{ marginLeft: 10, flex: 1 }}>
                                <div style={{
                                    color: "#385898",
                                    fontWeight: 600
                                }}>
                                    {props.name}
                                </div>
                                <div style={{ fontSize: 12, color: "gray" }}>{props.Time}</div>
                            </div>
                            
                            <div style={(props.isFake) ? {margin: 8, marginRight: 1, color: "red"} : {margin:8 , marginRight: 1, color:"green"}}  >{(props.isFake) ? "(Fake)" : "(True)"}</div>
                            <Popup trigger={<div> <FontAwesomeIcon style={(props.isFake) ? {margin: 12, color: "red"} : {margin:12 , color:"green"}} icon={(props.isFake) ? faThumbsDown : faThumbsUp} /> </div>}
                                position="left center"
                                on="hover"
                            >
                                <div>{"Our algorithm has detected that this article has a " + props.Percentage + "% chance of being fake"}</div>
                            </Popup>

                            <DropdownButton variant="light" title="">
                                <Dropdown.Item href="#/action-1">Share</Dropdown.Item>
                                <Dropdown.Item href="#/action-2">Delete</Dropdown.Item>
                            </DropdownButton>

                        </div>

                        <div style={{ width: "90%" }}>
                            <ReadMoreAndLess
                                charLimit={360}
                                readMoreText=" See More"
                                readLessText=" See Less"
                            >
                                {props.Text}
                            </ReadMoreAndLess>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
