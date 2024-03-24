import { useEffect, useState } from 'react';
import './Login.css'
import IButton from './IButton';
import axios from 'axios';
import bcrypt from 'bcryptjs' 

function Login({setLogin, switchLoginSignup}) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState()
    useEffect(() => {console.log(username)}, [username])
    const loginValidator = () => {
        console.log('loginattempt')
        axios.post(
            'http://127.0.0.1:5000/find_user',
            {
                user_data:{
                    'username': username,
                    'password':password
                }
            },
                {
                    headers: {
                        'content-type': 'application/json'
                      }
                }
        ).then((response)=>{
            if(!response.data['password']){
                console.log('invalid credentials')
                setError("Username or password is wrong")
                return
            }
            bcrypt.compare(
                password, response.data['password'], (err, data) => {
                    if(err) throw err
                    if(data){
                        setLogin(username)
                        console.log('Successful login')
                        return
                    }else{
                        console.log('Credentials are wrong')
                        setError("Username or password is wrong")
                        return
                    }
                }
            )
        })
    }
    return ( 
                <div className="login-box">
                    <div className="title-medium">
                        Log In
                    </div>
                    <div className='login-input-wrap'>
                        <input type='text' placeholder='Username' className='input-login' onChange={(e) => setUsername(e.target.value)}/>
                        <input type='password' placeholder='Password' className='input-login' onChange={(e) => setPassword(e.target.value)}/>
                        {error ? <div className='error'>{error}</div>:null}
                        <IButton buttonname={"Log In"} size={"medium"} inversion={"default"} onclick={loginValidator}/>
                    </div>
                    <div className='signup-switch'>
                        Don't have an account yet? 
                    </div>
                    <div className='sl-switch' onClick={switchLoginSignup}>Sign up here!</div>
                </div>

     );
}

export default Login;