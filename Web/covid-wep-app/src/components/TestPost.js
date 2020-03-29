import React from 'react'
import '../App.css';
import {Row, Textarea, Button} from 'react-materialize';

export default () => {

    return (
        <div style={{marginTop: 20}}>
            <div className="outerBox">
                <h6 style={{fontWeight: 500 }}>Test your URL</h6>
                <Row style={{ marginBotton: 0 }}>
                    <Textarea
                        s={12}
                        className="custom-textArea"
                        placeholder="Please write here..."
                        data-length={120}
                    />
                </Row>

                <div style={{height:"0"}}>
                    <Button
                        small
                        waves="light"
                        style={
                            {
                                backgroundColor: "royalBlue",
                                marginTop: -60
                            }
                        }
                    >
                        Test
                    </Button>
                </div>
            </div>
        </div>
    )
}
