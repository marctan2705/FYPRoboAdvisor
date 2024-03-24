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
import './sidebar.css'
import { PieChart } from '@mui/x-charts/PieChart';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Suggest from "./Suggest";
const drawerWidth = 400;

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  "& .MuiDrawer-paper": {
    width: drawerWidth,
    boxSizing: "border-box",
    backgroundColor: "white",
    color: 'white'
  },
}));
const riskq = {
  "question 1" : "abc",
  "question 2" : "abc",
  "question 3" : "abc"

}
const chats = ["Chat 1", "Chat 2", "Chat 3"]
function Sidebar({portfolio, username, questionnaire, onclicksuggest}) {
  console.log(questionnaire)
  const data = Object.entries(portfolio["details"]["composition"]).map((entry, index) => ({
    id: index,
    value: entry[1],
    label: entry[0],
  }));
  console.log(data)
  return (
    <StyledDrawer className='sidebar'variant="permanent" anchor="left">
      <div className="sidebar">
      <Accordion className="accordion">
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          User profile
        </AccordionSummary>
        <AccordionDetails>
        <div className="info-card-item"><span className="minititle">Networth: </span> ${questionnaire["answers"]["networth"]}</div>
          <div className="info-card-item"><span className="minititle">Experience: </span> {questionnaire["answers"]["experience"]}</div>
          <div className="info-card-item"><span className="minititle">Investment Horizon: </span> {questionnaire["answers"]["investment horizon"]} years</div>
          <div className="info-card-item"><span className="minititle">Risk: </span> {questionnaire["answers"]["risk"]} / 90 <span className="expand-risk">show more</span></div>
        </AccordionDetails>
      </Accordion>
      <Accordion className="accordion">
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Recommended Portfolio
        </AccordionSummary>
        <AccordionDetails>
        <div className="info-card-item"><span className="minititle">Portfolio name: </span>{portfolio["name"]}</div>
        <Accordion className="accordion">
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Portfolio Description
        </AccordionSummary>
        <AccordionDetails>
        {portfolio["details"]["Description"]}
        </AccordionDetails>
      </Accordion>
      <Accordion className="accordion">
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Portfolio Composition
        </AccordionSummary>
        <AccordionDetails>
        <PieChart
      series={[
        {
          data: data,
          cy:100
        },
      ]}
      width={250}
      height={300}
      position={{vertical:"start"}}
      slotProps={
        {
          legend:{
            direction: "column",
            position:{
              vertical:"bottom",
              horizontal: "bottom"
            },
            labelStyle: {
              fill:"black"
            }
        }
      }}
    />
        </AccordionDetails>
      </Accordion>
        
      </AccordionDetails>
      </Accordion>
      <Accordion className="accordion">
        <AccordionSummary
          expandIcon={<ExpandMoreIcon />}
          aria-controls="panel1-content"
          id="panel1-header"
        >
          Recommended Queries
        </AccordionSummary>
        <AccordionDetails>
        <Suggest onClick={onclicksuggest} />
        </AccordionDetails>
      </Accordion>
      </div>
      
    </StyledDrawer>
  );
}

export default Sidebar;