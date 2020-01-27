import React from 'react';
import '../css/login.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
  } from "react-router-dom";
import {userService as service} from '../service/user';
import { observer } from 'mobx-react';
import 'antd/es/message/style'
import { message, Button } from 'antd';
import { inject } from '../service/utils'


@inject({service})
@observer
export default class Reg extends React.Component {
  handleClick(event){
    event.preventDefault()
    const [username,mail,password]=event.target.form;
    this.props.service.reg(username.value,mail.value,password.value)
  }
  
  render(){
    if (this.props.service.loggedin)  {
      console.log('reg page',service.loggedinuser,'***********************')
      return <Redirect to="/" />;
    }
    return (
        <div className="login-page">
        <div className="form">
          <form className="login-form">
            <input type="text" placeholder="username"/>
            <input type="text" placeholder="mail"/>
            <input type="password" placeholder="password"/>
            <input type="password" placeholder="password again"/>
            <button onClick={this.handleClick.bind(this)}>注册</button>
            <p className="message">已经注册？<Link to='/login'>立即登录！！</Link></p>
          </form>
        </div>
      </div>
    );
  }
}
