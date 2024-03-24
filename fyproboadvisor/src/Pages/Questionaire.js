import { useEffect, useState } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import DropdownButton from 'react-bootstrap/DropdownButton';
import './Questionaire.css';
import IntensitySelector from './IntensitySelector.js';
import axios from 'axios';
import IButton from './IButton.js';
import Profiling from './Profiling.js';

function Questionaire({setQuestionaireDone, username}) {
    const [question, setQuestion] = useState(0)
    const [answers, setAnswers] = useState({})
    const [networth, setNetworth] = useState(0)
    const [risk, setRisk] = useState(new Array(6).fill(0))
    const [riskquestionnaire, setRiskQuestionnaire] = useState({})
    const manageRisk = (newrisk) => {
        // console.log("newrisk", newrisk)
        setRisk(newrisk)
        // console.log("start", newrisk)
        function sum(array) {
            // console.log("array", array)
            var total = 0; // Initialize total sum to 0
            for (let i = 0; i < array.length; i++) {
              total += parseInt(array[i]); // Add each element of array to total
            }
            console.log(total)
            return total; // Return the total sum
          }
        var newans = {...answers}
        newans["risk"] = sum(newrisk)
        // console.log("newans", newans)
        setAnswers(newans)
    }
    useEffect(
        ()=>{
            console.log("rq", riskquestionnaire)
        }, [riskquestionnaire]
    )
    const enterNetWorth = (e) => {
        setNetworth(e);
        var temp = answers;
        temp['networth'] = e;
        setAnswers(temp);
        console.log(answers);
    }
    const enterHorizon = (e) => {
        // setNetworth(e);
        var temp = answers;
        temp['investment horizon'] = e;
        setAnswers(temp);
        console.log(answers);
    }

    const enterExperience = (e) => {
        var temp = answers
        temp['experience'] = e;
        setAnswers(temp);
        console.log(answers);
    }
    const nextquestion = () => {
        setQuestion(question + 1);
    }
    const prevquestion = () => {
        if(question > 0){
            setQuestion(question - 1)

        }
    }
    const submit = () => {
        console.log("username", username)
        axios.post(
            'http://127.0.0.1:5000/add_questionnaire',
            {
              user_data: {
                username: username, 
                answers: answers
              }
            }, {
              headers: {
                'content-type': 'application/json'
              }
            }
        ).then(
            axios.post(
                'http://127.0.0.1:5000/add_assessment',
                {
                  user_data: {
                    username: username, 
                    riskAssessment: riskquestionnaire
                  }
                }, {
                  headers: {
                    'content-type': 'application/json'
                  }
                }
            ).then(
                axios.post(
                    'http://127.0.0.1:5000/get_portfolio',
                    {
                      user_data: {
                        "username": username,
                        "answers": answers
                      }
                    }, {
                      headers: {
                        'content-type': 'application/json'
                      }
                    }
                ).then(
                    (response) => {
                        console.log(response)
                        setQuestionaireDone({
                            username: username,
                            answers: answers
                        })
                    }
                )
            )
        )

    }
    const handlenext = () => {
        if(question ==9){
            submit()
        }else{
            nextquestion()
        }
    }
    useEffect(
        () => {
            console.log("answers", answers)
        }
        , [answers]
    )
    return ( 
        <div id="qp" className='questionaire-page'>
            {
            question === 0
            ?
            <div className='questionaire-box'>
                <div className='question-header'>
                    What is your net worth?
                </div>
                <input type='number' className = 'question-input' onChange={(e)=>{enterNetWorth(e.target.value)}}>

                </input>
            </div>
            :
            question === 1
            ?
            <div className='questionaire-box'>
                <IntensitySelector title={'How much experience do you have?'} updater={enterExperience}/>
            </div>
            :
            question === 2
            ?
            <div className='questionaire-box'>
                <div className='question-header'>
                    What is your investment horizon in terms of years?
                </div>
                <input type='number' className = 'question-input' onChange={(e)=>{enterHorizon(e.target.value)}}>
                </input>
            </div>
            :
            question === 3
            ?
            <div className='questionaire-box'>
                <div className='question-header'>
                    Risk Assessment
                </div>
                This portion will assess your risk adversity to better customise your portfolio. Please answer to your best ability.
            </div>
            :
            <div className='questionaire-box'>
                <Profiling question={question - 3} setRisk={manageRisk} rq={riskquestionnaire} setrq={setRiskQuestionnaire} risk={risk}/>
            </div>
            }
            <div className='questionaire-buttons'>
                <IButton buttonname={'Back'} size={'medium'} inversion={'inverse'} onclick={prevquestion} />
                <IButton buttonname={'Next'} size={'medium'} inversion={'default'} onclick={handlenext} />
            </div>
        </div>
     );
}

export default Questionaire;