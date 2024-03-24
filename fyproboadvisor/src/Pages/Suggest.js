import { styled } from "@mui/material/styles";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import DraftsIcon from "@mui/icons-material/Drafts";
import DeleteIcon from "@mui/icons-material/Delete";
import ReportIcon from "@mui/icons-material/Report";
import pin1 from './assets/pin1.png'
import './suggest.css'
import QueryRec from "./QueryRec";
const drawerWidth = 400;

const queries = [
    "Can you help me find some news on [insert stock] Stocks?",
    "Can you help me analyse recent news on [insert stock]",
    "What are your thoughts on [insert stock]",
    "Can you recommend me some [products] in [country]. Summarise the the different options for me.",
    "Can you help me optimise the stoc portion of my portfolio?",
    "can you help me analyse the basket recommended to me?"
]
function Suggest({onClick}) {
    return ( 
        <div>
            {/* <div className="queryholder"> */}
            <div>
                The queries below are suggested for the best results! Click any query below to use the template, and replace parameters in [] with your preferred parameters:
            </div>
            {
                queries.map(
                    (query) =>
                    {
                       return( <QueryRec onClick={onClick} Query={query} />)
                    }
                )
            }
            {/* </div> */}

            </div>
     );
 }
 
 export default Suggest;