import React from 'react'
import {Container, Row, Col} from 'react-materialize';
import TestPost from './TestPost';
import Post from './Post';

export default () => {

    /*
    A post object will contain:
    -Name
    -URL
    -Picture (url)
    -Text
    -Boolean to indicate if fake or not
    -Percentage
    */

    let posts = []
    
    let test = {
        name: "Ricardo Milos",
        Picture: "https://i.kym-cdn.com/entries/icons/original/000/010/843/ricardo.jpg",
        Text: "Ricardo Milos is a Brazilian adult model known for his erotic dance video. His dance video, often referred to as Danced Like a Butterfly, inspired a series of MAD/animated videos on the Japanese video-hosting site Nico Nico Douga (NND) in mid-to-late 2011.The series helped to establish Milos as a character in the Gachimuchi/wrestling series. In mid-to-late 2018, people online began using Milos’ dance in bait-and-switch videos in reaction to the application TikTok.",
        isFake: false,
        Percentage: "100%",
        Time: "69 min ago"
    }

    let test1 = {
        name: "Pepe The Frog",
        Picture: "https://i.kym-cdn.com/entries/icons/original/000/017/618/pepefroggie.jpg",
        Text: "Pepe the Frog is an anthropomorphic frog character from the comic series Boy’s Club by Matt Furie. On 4chan, various illustrations of the frog creature have been used as reaction faces, including Feels Good Man, Sad Frog, Angry Pepe, Smug Frog and Well Meme'd.",
        isFake: true,
        Percentage: "69%",
        Time: "420 min ago"
    }

    posts.push(test)
    posts.push(test1)

    return (
        <Container>
            <Row>
                <Col m={12} s={12}>
                    <TestPost />
                    {
                        posts.map(
                            (object, index) => {
                                return <Post
                                    key={index}
                                    name={object.name} 
                                    URL={object.URL}
                                    Picture={object.Picture}
                                    Text={object.Text}
                                    isFake={object.isFake}
                                    Percentage={object.Percentage}
                                    Time={object.Time}
                                  />          
                            }
                        )
                    }
                </Col>
            </Row>
        </Container>
    )
}
