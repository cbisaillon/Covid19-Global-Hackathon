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

    const iconStyle = {
        margin: 12
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

                            <Popup trigger={<div> <FontAwesomeIcon style={iconStyle} icon={(props.isFake) ? faThumbsDown : faThumbsUp} /> </div>}
                                position="left center"
                                on="hover"
                            >
                                <div>{(props.isFake) ? "Our algorithm has detected that this article has a " + props.Percentage + " of being fake" : "Our algorithm has detected that this article has a " + props.Percentage + " of being true"}</div>
                            </Popup>

                            <DropdownButton variant="light" title="">
                                <Dropdown.Item href="#/action-1">Share</Dropdown.Item>
                                <Dropdown.Item href="#/action-2">Delete</Dropdown.Item>
                            </DropdownButton>

                        </div>

                        <div style={{ width: "90%" }}>
                            <ReadMoreAndLess
                                charLimit={300}
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
