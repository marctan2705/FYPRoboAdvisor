import { useState } from "react";
import './Ibutton.css'

function IButton({buttonname, onclick, size, inversion}) {
    const [buttonClass, setButtonClass] = useState("button-" + size + " button-" + inversion)
    return ( 
        <div className={buttonClass} onClick={onclick}>
            {buttonname}
        </div>
     );
}

export default IButton;