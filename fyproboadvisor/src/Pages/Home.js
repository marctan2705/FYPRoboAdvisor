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
import { useState } from "react";
import Questionaire from "./Questionaire";

function Home({setlogin, isLoggedIn}) {
    const [home, setHome] = useState(false)
    const [loginSignup, setLoginSignup] = useState(true);
    const switchLoginSignup = () => {
      setLoginSignup(!loginSignup)
    }
    const loginpage = () => {
        setHome(false)
        setLoginSignup(false)
        console.log("home", home)
    }
    const signuppage = () => {
        setHome(false)
        setLoginSignup(true)
        // console.log('signup')
    }
    const homepage = () => {
        setHome(true)
    }
    return ( 
        <div>
            <Header sethome={homepage} setlogin={loginpage} setsignup={signuppage} isin={false}/>
            <div className="home-body">
            { home ?

                <div className="home-content">
                    <div className="title">
                        Engage with our RoboAdvisor
                    </div>
                    <div className="title-content">
                    Our robo-advisor uses state of the art AI and LLM tools trained with advanced financial techniques and models to provide you with the best wealth management advice in the industry.
                    </div>
                    <IButton buttonname="Get Started >>" size={'large'} inversion={'default'} onclick={signuppage}/>
                </div>
                :
            !loginSignup ? 
            <Login switchLoginSignup={switchLoginSignup} setLogin={setlogin}/>
            :
            loginSignup ?
            <Signup setLogin={setlogin} switchLoginSignup={switchLoginSignup}/>
                :
                null
        }
                <div className="home-robot-pins">
                    <img src={robot} className="robot" />
                    <div className="pins">
                        <Pin image={pin1} content={"Customiseable to your needs"}/>
                        <Pin image={pin2} content={"Modern and accurate financial models"}/>
                        <Pin image={pin3} content={"Human-like interaction"}/>
                    </div>
                </div>
            </div>
            
        </div>
     );
}

export default Home;