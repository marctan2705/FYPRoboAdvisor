import React, { useCallback, useEffect, useState } from 'react';
import axios from 'axios';
import './ChatApp.css';
import AnswerBox from './AnswerBox';

const ChatApp = () => {
  const modes = ["Light", "Dark"]
  const [mode, setMode] = useState(0)
  const [curtext, setCurtext] = useState("")
  const [messages, setMessages] = useState([
    {
      "by": "user", "content":"user hi"
    }, {"by" : "chatbot", "content": "Hi!"}
  ])

  const getResponse = useCallback(
    (question, newarray) => {
      axios.post('http://127.0.0.1:5000/get_response',
      {
        chatters: question
      }, {
        headers: {
          // 'application/json' is the modern content-type for JSON, but some
          // older servers may use 'text/json'.
          // See: http://bit.ly/text-json
          'content-type': 'application/json'
        }
      }) .then((response) => {
        console.log(response);
        newarray.push({"by": "chatbot", "content": response.data["reply"]})
        setMessages([...newarray]);
        // console.log(messages)
          // Handle data
      })
    }, [messages]
  )




  // function getResponse(question){
  //     axios.post('http://127.0.0.1:5000/get_response',
  //     {
  //       chatters: question
  //     }, {
  //       headers: {
  //         // 'application/json' is the modern content-type for JSON, but some
  //         // older servers may use 'text/json'.
  //         // See: http://bit.ly/text-json
  //         'content-type': 'application/json'
  //       }
  //     }) .then((response) => {
  //       // console.log(messages);
  //       var newarray = [...messages]
  //       console.log("newarray", newarray)
  //       newarray.push({"by": "user", "content": response.data["reply"]})
  //       setMessages([...newarray]);
  //       // console.log(messages)
  //         // Handle data
  //     })
  //     // axios.get(
  //     //   'http://127.0.0.1:5000/'
  //     // ).then((response)=>{console.log(response)})

  //   }
  function handlekeydown(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      var newarray = [...messages]
      newarray.push({"by": "user", "content": curtext})
      // console.log(newarray)
      setMessages([...newarray]);
      getResponse(curtext, newarray);
      document.getElementById("textarea").value="";
      setCurtext("");
    }
  }
  useEffect(
    () => {console.log(curtext)}, [curtext]
  )

  useEffect(
    () => {console.log(mode)}, [mode]
  )
  return (
    <div className={'bodyDark'} onClick = {() => setMode((mode + 1)%2)}>
      <div className='conversationBox'>
        {
          messages.map(
            (message)=>
                {
                  return (
                    <div className={'messageBox' + message.by}>
                      <div className='message'>{message.content}</div>
                    </div>
                  )
                }
          )
        }
      </div>
      <div className='footer'>
        <AnswerBox id={"textarea"} onKeyDown={handlekeydown} setCurtext={setCurtext}/>
      </div>
    </div>
  );
};

export default ChatApp;