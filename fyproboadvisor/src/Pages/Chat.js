import { useCallback, useEffect, useState } from 'react';
import './Chat.css'
import Sidebar from './Sidebar';
import axios from 'axios';
import pin3 from './assets/pin3.png'
import robot from './assets/robot.png'
import Suggest from './Suggest';
import {marked} from 'marked'
function Chat({questionairedone, username}) {
    const [curtext, setCurtext] = useState("")
    const [boxheight, setBoxheight] = useState("30px")
    const [portfolio, setPortfolio] = useState()
    const [x, setx] = useState(0)
    const qans = questionairedone["answers"]
    var val = 0
    const getMarkdown = (FORM_INPUT) => {
      if (FORM_INPUT) {
        let markdown = marked(FORM_INPUT , { sanitize: true })
        return { __html: markdown }
      }
}
    const [messages, setMessages] = useState([
      {"role":"system", "content":`You are a financial assistant specialised in giving advice on how to allocate a portfolio with minimum risk and providing information about various stocks. Your client has a networth of ${qans["networth"]}, a ${qans["risk"]} risk tolerance and a ${qans['experience']} level of experience.`},
      {"role": "chatbot", "content":
    "Hi! I am your friendly financial Assistant, here's a quick guide on how you can get started: \n \n1. On the left side of the screen, you can access various features.\n1a. You can click on User Profile to view your profiling details.\n1b. You can click the Recommended portfolio accordion to view the portfolio breakdown that is tailored to your profiling details.\n1c. Recommended queries are provided as templates. You can click any of the recommended queries to load the template in the chatbox. Feel free to replace the paramters wrapped in [ ] with what you are looking for! \n2. You can type any queries into the chatbox below. Hit enter on your keyboard to send the query over to the bot!"
    }
    ])
    useEffect(
        () => {
            if(Math.ceil(curtext.length/ 72) < 7){
            setBoxheight(String(Math.floor(curtext.length/ 72)*15 + 30)+"px")}else{setBoxheight(7*15+30)}
        }, [curtext]  
    )
    useEffect(    
      () => {
        val += 1
        if(val == 1){ 
          axios.post('http://127.0.0.1:5000/get_context',
        {
          chatters: {"role":"system", "content":`You are a financial assistant specialised in giving advice on how to allocate a portfolio with minimum risk and providing information about various stocks. Your client has a networth of ${qans["networth"]}, a ${qans["risk"]} risk tolerance and a ${qans['experience']} level of experience. you have access to tools that can help you get various information. you aren't very good at calculations yourself, so you should only performed using the handy tools given to you.`}
        }, {
          headers: {
            'content-type': 'application/json'
          }
        }) .then(
          axios.post('http://127.0.0.1:5000/retrieve_portfolio',
          {
            user_data: {
              "username": username
            }
          }
          , {
            headers: {
              'content-type': 'application/json'
            }
          }) .then(
            (response) => {console.log("res", response); setPortfolio(response.data["portfolio"]); setx(1)}
            )
          )
        }
      }, []
    )
    const getResponse = useCallback(
      (curtext, newarray) => {
        console.log(newarray)
        axios.post('http://127.0.0.1:5000/get_response',
        {
          chatters: newarray
        }, {
          headers: {
            'content-type': 'application/json'
          }
        }) .then((response) => {
          console.log(response);
          newarray.push({"role": "chatbot", "content": response.data["reply"]})
          setMessages([...newarray]);
        })
      }, [messages]
    )

    function handlekeydown(e) {
      if (e.key === 'Enter') {
        e.preventDefault();

        // Prepare the new state data but don't wait for the state to update
        var newarray = [...messages, {"role": "user", "content": curtext}];

        // Call setMessages to update the state
        setMessages(newarray);

        // Immediately call getResponse with the new array
        // This assumes getResponse does not rely on the updated state from a re-render
        getResponse(curtext, newarray);

        // Reset your input
        document.getElementById("textarea").value = "";
        setCurtext("");
      }
    }
    function changeQuery(e){
      document.getElementById("textarea").value = e;
      setCurtext(e)
    }
    useEffect(
      () => {console.log(curtext)}, [curtext]
    )
    return ( 
        <div className='chat'>
            {x==1 ? <Sidebar onclicksuggest={changeQuery} portfolio={portfolio} username={username} questionnaire={questionairedone}/> : null}
            <div className='chat-content'>
            <div className='message-box'>
            {
                    messages.map(
                        (message) => {
                            return(
                              
                                message['role'] == "system" ?
                                null :
                                message['role'] == "user"
                                ?
                                <>
                                <hr className='message-divider'></hr>
                                <div className='message-area-user'>
                                <img className="message-icon" src={pin3} />
                                <div className="message-content-user">
                                    <div dangerouslySetInnerHTML={getMarkdown(message["content"])} />
                                </div>
                                </div>
                                </>
                                :
                                <>
                                <hr className='message-divider'></hr>
                                <div className='message-area-chatbot'>
                                <div className="message-content-chatbot">
                                <div dangerouslySetInnerHTML={getMarkdown(message["content"])} />
                                </div>
                                <img className="message-icon-robot" src={robot} />
                                </div>
                                </>

                            )
                        }
                    )
                }
            </div>
            <textarea placeholder="Type your query here..." id='textarea' className='chat-input' style={{height:boxheight}} onKeyDown={handlekeydown} onChange={(e) => setCurtext(e.target.value)}>
            </textarea>
            </div>
            {/* <Suggest onClick={changeQuery}/> */}
        </div>
     );
}

export default Chat;