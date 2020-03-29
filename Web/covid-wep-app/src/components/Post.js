import React from 'react'
import { Icon } from 'react-materialize';
import { Dropdown, DropdownButton } from 'react-bootstrap';
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

                            <DropdownButton id="dropdown-custom-3" title={<Icon>more_vert</Icon>}>
                                <Dropdown.Item href="#/action-1">Action</Dropdown.Item>
                                <Dropdown.Item href="#/action-2">Another action</Dropdown.Item>
                                <Dropdown.Item href="#/action-3">Something else</Dropdown.Item>
                            </DropdownButton>



                        </div>

                        <div style={{ width: "95%" }}>
                            {props.Text}
                        </div>


                    </div>
                </div>
            </div>
        </div>
    )
}
