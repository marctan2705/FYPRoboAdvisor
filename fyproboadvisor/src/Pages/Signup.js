import { useEffect, useState } from 'react';
import './Login.css'
import bcrypt from 'bcryptjs' 
import axios from 'axios';
import IButton from './IButton';
// import {useDispatch} from 'react-redux';
// import {login} from './features/userSlice'

function Signup({setLogin, switchLoginSignup}) {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [username, setUsername] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [equalpassword, setEqualPassword] = useState(true)
    const [confirmClass, setConfirmClass] = useState('input-login')
    const [error, setError] = useState("")
    // const dispatch = useDispatch();
    const create_user = (username, password, email) => {
        bcrypt
        .genSalt(10)
        .then(salt => {
          console.log('Salt: ', salt)
          return bcrypt.hash(password, salt)
        })
        .then(hash => {
            axios.post('http://127.0.0.1:5000/add_user',
            {
              user_data: {
                "email": email,
                "username": username,
                "password": hash
              }
            }, {
              headers: {

                'content-type': 'application/json'
              }
            }) .then((response) => {
                console.log("hi")
              console.log(response["data"]);
              if(response["data"] === "Successful"){
                setLogin(username);
                return;
              }
              console.log("here");
              setError(response["data"])
              return;

            })
        })
        .catch(err => {console.error(err.message)})
    }
    useEffect(
        ()=>{
            const comparison = passwordCompare(password, confirmPassword);
            console.log(comparison)
            setEqualPassword(comparison);
            if(comparison){
                setConfirmClass('input-login')
            }else{
                setConfirmClass('input-login input-login-false')
            }
            return;
        }, [password, confirmPassword]
    )
    const passwordCompare = (password, confirmPassword) => {
        return password === confirmPassword;
    }
    const signupValidator = () => {
        if((email != "" && !email.includes("@")) || (password && password.length < 8) || (equalpassword && password == equalpassword)){
            return
        }
        if(equalpassword === true && password !== '' && username !== '' && email !== ''){
            create_user(username, password, email);
            return
        }else{
            console.log('Signup Issue')
            return
        }
    }
    return ( 
        <div className="login-box">
                <div className="title-medium">
                    Sign up
                </div>
                <div className='login-input-wrap signup-input-wrap'>
                    <input type='text' placeholder='Email' className='input-login' onChange ={(e) => setEmail(e.target.value)} />
                    {email != "" && !email.includes("@") ? <div className="error">Please use a valid email</div> : null}
                    <input type='text' placeholder='Username' className='input-login' onChange ={(e) => setUsername(e.target.value)}/>
                    <input type='password' placeholder='Password' className='input-login' onChange ={(e) => setPassword(e.target.value)}/>
                    {password && password.length < 8 ? <div className="error">Please use a password of at least length 8</div> : null}
                    <input type='password' placeholder='Confirm Password' className={confirmClass} onChange ={(e) => setConfirmPassword(e.target.value)}/>
                    {confirmPassword && password != confirmPassword ? <div className="error">Passwords do not match</div> : null}
                    {error ? <div className='error'>{error}</div>:null}
                    <IButton buttonname={"Sign up"} onclick={signupValidator} size={"medium"} inversion={"default"}/>
                </div>
                <div className='signup-switch'>
                    Have an account? 
                </div>
                <div className='sl-switch' onClick={switchLoginSignup}>Log in here!</div>
        </div>
     );
}

export default Signup;