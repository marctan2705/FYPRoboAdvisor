import { useEffect } from "react";
import "./AnswerBox.css"
function AnswerBox({setCurtext, onKeyDown, id}) {

    return ( 
        <div className="Answerbox">
            <div className="ansflex">
                    <textarea id={id} className="anstext" placeholder="Ask a Question here" onChange={(e) => setCurtext(e.target.value)} onKeyDown={(e)=>onKeyDown(e)}/>
            </div>
        </div>
     );
}

export default AnswerBox;
