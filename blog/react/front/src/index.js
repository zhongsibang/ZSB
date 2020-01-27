import React from 'react';
import ReactDom from 'react-dom';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Login from './componet/login';
import Reg from './componet/reg';
import Pub from './componet/pub';
import {Detail} from './componet/detail'
import { observer } from 'mobx-react';
import { observable } from 'mobx';
import {userService as service} from './service/user'
import { Menu, Icon,Layout } from 'antd';
import 'antd/es/menu/style'
import 'antd/es/icon/style'
import { Llist } from './componet/list';
const { Header, Footer, Content } = Layout;
import { LocaleProvider } from 'antd';
import zh_CN from 'antd/es/locale-provider/zh_CN';


class Root extends React.Component{
  render(){
    //console.log('index page',service.loggedinuser)
    return(
      <Router>
      <Layout>
      <div>
      <Header>
        <div className="logo" />
        <Menu theme="dark"
        mode="horizontal"
        defaultSelectedKeys={['2']}
        style={{ lineHeight: '64px' }}>
          <Menu.Item key="home"><Link to="/"><Icon type="home" />主页</Link></Menu.Item>
          <Menu.Item key="login"><Link to="/login"><Icon type="login" />登录</Link></Menu.Item>
          <Menu.Item key="reg"><Link to="/reg"><Icon type="user" />注册</Link></Menu.Item>
          <Menu.Item key="pub"><Link to="/pub"><Icon type="upload" />发布</Link></Menu.Item>
          <Menu.Item key="list"><Link to="/list"><Icon type="bars" />文章列表</Link></Menu.Item>
          <Menu.Item key="about"><Link to="/about"><Icon type="solution" />关于</Link></Menu.Item>
        </Menu>
        </ Header>
        <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
        <Content style={{ padding: '0 50px' }}>
        <Switch>
          <Route path="/login">
            <Login />
          </Route>
          <Route path="/reg">
            <Reg />
          </Route>
          <Route path="/pub">
            <Pub />
          </Route>
          <Route path="/list" component={Llist} />
          <Route path="/post/:id" component={Detail} /> 
        </Switch>
        </Content>
        </div>
        <Footer style={{ textAlign: 'center' }}>Made by ZSB in 2020</Footer>
      </div>
      </Layout>
    </Router>
    );
  }
}

@observer
class Logstatus extends React.Component{
  render() {
    if (service.loggedin) {
      return(
      <span>Logged User:
      {service.loggedinuser.userid},
      {service.loggedinuser.username},
      {service.loggedinuser.mail},
      {service.loggedinuser.logdate.toString()}
      </span>
      )
    }
    return (
      <span>No User Login !!!</span> 
    //<span>Seconds passed: { timerData.secondsPassed } </span> 
    )
  }
};
ReactDom.render(<LocaleProvider locale={zh_CN}><Root /></LocaleProvider>,document.getElementById('zsb'));
ReactDom.render(<Logstatus />,document.getElementById('logstatus'));


