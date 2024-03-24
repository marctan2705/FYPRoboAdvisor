import logo from './logo.svg';
import './App.css';
import ChatApp from './Pages/ChatApp';
import Login from './Pages/Login'
import { useEffect, useState } from 'react';
import Signup from './Pages/Signup';
import Questionaire from './Pages/Questionaire';
import Home from './Pages/Home';
import QuestionairePage from './Pages/QuestionairePage';
import Chat from './Pages/Chat';
import axios from "axios";
import Sidebar from './Pages/Sidebar';
import Suggest from './Pages/Suggest';
// import { useSelector } from 'react-redux';
// import { selectUser } from './Pages/features/userSlice';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [questionairedone, setQuestionaireDone] = useState(false);
  useEffect(
    ()=>{
      if(isLoggedIn == false){
        return
      }
      else{
        console.log(isLoggedIn)
      axios.post(
        'http://127.0.0.1:5000/get_questionnaire',
            {
                user_data:{
                    'username': isLoggedIn
                }
            },
                {
                    headers: {
                        'content-type': 'application/json'
                      }
                }
      ).then(
        (response) => {
          console.log(response)
          if(response.data.questionnaire == false){
            console.log("here")
            return
          }else{
            setQuestionaireDone(response.data)
          }
        }
      )}
    }, [isLoggedIn]
  )
  // const user = useSelector(selectUser)
  return (
    // <QuestionairePage setQuestionaireDone={setQuestionaireDone} />
    <div>
     {!isLoggedIn ? <Home isLoggedIn={isLoggedIn} setlogin={setIsLoggedIn}/> : questionairedone ? <Chat username={isLoggedIn} questionairedone = {questionairedone}/> : <QuestionairePage setQuestionaireDone={setQuestionaireDone} username={isLoggedIn}/>}
     {/* <Suggest/> */}
    </div>
  );
}

export default App; 
