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
//import { func } from 'prop-types';
import { inject } from '../service/utils'



@inject({service}) //Login = injet(Login)(service)
@observer    /**mobx模块，定义观察者，观察user.UserService.login内的observerable对象loggedin */
export default class Login extends React.Component {
  /**定义click触发的事件 */
  handleClick(event){
      event.preventDefault()
      /**不能使用return false，阻止时间默认行为，采用异步方式 */
      /**
      console.log(event,'1111111111111')
      console.log(event.target.form[0])
      console.log(event.target.form[1])
      const [mail,password] = event.target.form
      console.log(mail.value,password.value) 
      */
      /**event.target.form 可以获取表单数据 */
      const [mail,password] = event.target.form
      this.props.service.login(mail.value,password.value)
      /**这个类的属性添加了service，就是UserService，再调用内部login函数 */
    }
  
    render(){
        //console.log(this.props.service.loggedin,'Mobx!!!!!!!!!!!!!!')
        if (this.props.service.loggedin)  {
          console.log('login page',service.loggedinuser,'***********************')
          return <Redirect to="/" />;
        }/**前端页面跳转，如果登录成功，跳转到主界面 */
        let em =this.props.service.errm
        /**需要引起变化才会触发重绘，componetDidCatch才有用 */
        return (
            <div className="login-page">
            <div className="form">
              <form className="login-form">
                <input type="text" placeholder="mail" />
                <input type="password" placeholder="password" />
                <button onClick={this.handleClick.bind(this)}>登录</button>
                <p className="message">未注册？<Link to='/reg'>立即注册！</Link></p>
              </form>
            </div>
          </div>
        );
    }   

    /**官方建议属性或者state的修改不要放在render函数中，所以放在生命周期的结束部分 */
    componentDidUpdate(preProps,preState){
        if (preProps.service.errm===false) {
              message.info('用户名密码错误！', 5,()=>preProps.service.errm=true);
        }
    } 
  }