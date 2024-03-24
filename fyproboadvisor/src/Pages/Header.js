import * as React from "react";
 
// importing material UI components
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import IButton from "./IButton";

function  Header({sethome, setlogin, setsignup, isin}) {
    return ( 
        <AppBar position="fixed" style={{background: '#000000'}}>
            <Toolbar>
                <Typography
                    variant="h6"
                    component="div"
                    sx={{ flexGrow: 1 }}
                >
                    <div style={{cursor: "pointer", font_weight:'bold'}}onClick={sethome}><b>InvWealthGPT</b></div>
                </Typography>
                { !isin ?
                <>
                <IButton buttonname={"Login"} size={'small'} inversion={'inverse'} onclick={setlogin}/>
                <IButton buttonname={"Sign up"} size={'small'} inversion={'default'} onclick={setsignup}/> </>: null}
            </Toolbar>
        </AppBar>
     );
}

export default  Header;