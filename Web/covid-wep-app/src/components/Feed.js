import React from 'react'
import { Container, Row, Col } from 'react-materialize';
import TestPost from './TestPost';
import Post from './Post';
import { trackPromise } from 'react-promise-tracker';
import axios from 'axios';
import { usePromiseTracker } from "react-promise-tracker";
import Loader from 'react-loader-spinner';
import InfiniteScroll from 'react-infinite-scroll-component';


export default class Feed extends React.Component {

    /*
    A post object will contain:
    -Name
    -URL
    -Picture (url)
    -Text
    -Boolean to indicate if fake or not
    -Percentage
    */
    constructor(props) {
        super(props)

        this.state = {
            posts: [],
        }
    }

    componentDidMount() {

        const config = {
            headers: { 'Access-Control-Allow-Origin': '*' }
        };
        trackPromise(
            axios.get('https://cors-anywhere.herokuapp.com/https://4ua127bd2e.execute-api.us-east-2.amazonaws.com/api/post-list?per_page=10', config)
                .then(res => {
                    this.setState({ posts: res.data })
                })
        );

    }

    fetchMoreData = () => {
        const config = {
            headers: { 'Access-Control-Allow-Origin': '*' }
        };
        
        trackPromise(
           axios.get('https://cors-anywhere.herokuapp.com/https://4ua127bd2e.execute-api.us-east-2.amazonaws.com/api/post-list?per_page=1', config)
            .then(res => {
                let joined = this.state.posts.concat(res.data);
                this.setState({ posts: joined })
            })  
        );
    }

    

    render() {

        const LoadingIndicator = props => {
            const { promiseInProgress } = usePromiseTracker();
            
            return (
              promiseInProgress && 
                <div
                style={{
                width: "100%",
                height: "100",
                display: "flex",
                justifyContent: "center",
                alignItems: "center"
              }}
            >
              <Loader type="ThreeDots" color="royalblue" height='100' width='100' />
            </div>
              );  
             }


        return (
            <Container>
                <Row>
                    <Col m={12} s={12}>
                        <TestPost />
                        <InfiniteScroll
                            dataLength={this.state.posts.length}
                            next={this.fetchMoreData}
                            hasMore={true}
                            loader={<LoadingIndicator />}
                        >
                            {
                            this.state.posts.map(
                                (object, idx) => (
                                    <Post
                                        key={idx}
                                        name={object.user.name}
                                        URL={object.post.link}
                                        Picture={object.user.profile_pic}
                                        Text={object.post.text}
                                        isFake={object.is_fake}
                                        Percentage={Math.ceil(object.chance*100)}
                                        Time={(idx >= 60) ? Math.ceil(idx/60)+" hrs ago" : idx+" min ago"}
                                    />
                                )
                            )
                        }
                        </InfiniteScroll>    
                    </Col>
                </Row>
            </Container>
        )
    }

}
