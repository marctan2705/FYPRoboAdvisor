import { useRadioGroup } from '@mui/material/RadioGroup';
import { FormControl, RadioGroup, Radio, FormControlLabel } from '@mui/material';
import * as React from 'react';
import { pink } from '@mui/material/colors';

function Profiling({question, risk, setRisk, setrq, rq}) {
    const questions = {
        "1": {
          "text": "There is a potential for loss when investing. What portion of your overall investable assets would you typically set aside for investing?",
          "options": [
            {"key": "a", "text": "Between >0% and 50%", "score": 0},
            {"key": "b", "text": "Over 50%", "score": 14}
          ]
        },
        "2": {
          "text": "What level of risk are you willing to accept in order to achieve your expected returns?",
          "options": [
            {"key": "a", "text": "I am not willing to accept any loss", "score": 0},
            {"key": "b", "text": "I am willing to accept a minimal amount of loss", "score": 5},
            {"key": "c", "text": "I am willing to accept a moderate amount of loss", "score": 9},
            {"key": "d", "text": "I am willing to accept a high amount of loss", "score": 14}
          ]
        },
        "3": {
          "text": "What is your primary investment goal?",
          "options": [
            {"key": "a", "text": "Capital preservation", "score": 0},
            {"key": "b", "text": "A regular stream of stable income", "score": 4},
            {"key": "c", "text": "A combination of income and capital growth", "score": 7},
            {"key": "d", "text": "Achieve substantial long term capital growth", "score": 11},
            {"key": "e", "text": "High capital appreciation", "score": 14}
          ]
        },
        "4": {
          "text": "What is the maximum potential loss and potential upside in a given time horizon (i.e. 1 year) that you would be most comfortable with?",
          "options": [
            {"key": "a", "text": "I am willing to accept a potential loss of 13% for 13% potential upside.", "score": 0},
            {"key": "b", "text": "I am willing to accept a potential loss of 19% for 19% potential upside.", "score": 4},
            {"key": "c", "text": "I am willing to accept a potential loss of 25% for 25% potential upside.", "score": 7},
            {"key": "d", "text": "I am willing to accept a potential loss of 31% for 31% potential upside.", "score": 11},
            {"key": "e", "text": "I am willing to accept a potential loss of 38% for 38% potential upside.", "score": 14}
          ]
        },
        "5": {
          "text": "How would you react to a significant drop in the value of your investments?",
          "options": [
            {"key": "a", "text": "I will sell the investments if the drop in value is small.", "score": 0},
            {"key": "b", "text": "I will sell the investments if the drop in value is large.", "score": 5},
            {"key": "c", "text": "I will sell some of the investments if the drop in value is large, and wait for the remaining investments to recover in value.", "score": 9},
            {"key": "d", "text": "I will not sell the investments, regardless of the drop in value, and will buy more to capitalize on the cheaper price.", "score": 14}
          ]
        },
        "6": {
          "text": "What range of annual return volatility are you comfortable with?",
          "options": [
            {"key": "a", "text": "Between -4% and 4%", "score": 0},
            {"key": "b", "text": "Between -7% and 7%", "score": 4},
            {"key": "c", "text": "Between -10% and 10%", "score": 7},
            {"key": "d", "text": "Between -13% and 13%", "score": 11},
            {"key": "e", "text": "More than -13% and more than +13%", "score": 14}
          ]
        }
      }
      var q = questions[question]
      var reversecheck = {}
      q["options"].map(
        (option) => {
            reversecheck[option.key] = {
                "text": option.text,
                "score": option.score
            }
        }
      )
    //   console.log(q)
    const handleChange = (e) => {

        var newrisk = [...risk]
        newrisk[question - 1] = reversecheck[e.target.value]["score"]
        // console.log("newrisk1", newrisk)
        var rq2 = {...rq}
        rq2[q["text"]] = reversecheck[e.target.value]["text"]
        // console.log("check", rq2[q["text"]])
        setRisk(newrisk)
        setrq(rq2)
        return
    }
    return ( 
        <div>
            <div className='question-header'>
            {q.text}
            </div>
            <FormControl>
            <RadioGroup
                aria-labelledby="demo-controlled-radio-buttons-group"
                name="controlled-radio-buttons-group"
                onChange={handleChange}
                // value={selected}
            >
                {
                    q.options.map(
                        (option) => {
                            return(
                                <FormControlLabel value={option.key} control={<Radio
                                    sx={{
                                      color: pink[800],
                                      '&.Mui-checked': {
                                        color: pink[600],
                                      },
                                    }}
                                    
                                    />} label={option.text}/>
                            )
                        }
                    )
                }
                
            </RadioGroup>
            </FormControl>
        </div>
     );
}

export default Profiling;