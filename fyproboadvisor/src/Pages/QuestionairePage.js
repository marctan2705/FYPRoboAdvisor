import Header from "./Header";
import "./Home.css"
import IButton from "./IButton";
import robot from "./assets/robot.png"
import Pin from "./Pin"
import pin1 from "./assets/pin1.png"
import pin2 from "./assets/pin2.png"
import pin3 from "./assets/pin3.png"
import Login from "./Login";
import Signup from "./Signup";
import { useEffect, useState } from "react";
import Questionaire from "./Questionaire";
function QuestionairePage({setQuestionaireDone, username}) {
    return ( 
    <div>
        <Header sethome={null} isin={true}/>
        <div className="home-body">

            <div className="home-content">
                <div className="title">
                    Questionaire
                </div>
                <div className="title-content">
                    Help answer this questionaire so we can provide you a personalised portfolio.
                </div>
                <Questionaire setQuestionaireDone={setQuestionaireDone} username={username}/>
            </div>
            <div className="home-robot-pins">
                <img src={robot} className="robot" />
                <div className="pins">
                    <Pin image={pin1} content={"Customiseable to your needs"}/>
                    <Pin image={pin2} content={"Modern and accurate financial models"}/>
                    <Pin image={pin3} content={"Human-like interaction"}/>
                </div>
            </div>
        </div>
    </div> );
}

export default QuestionairePage;
