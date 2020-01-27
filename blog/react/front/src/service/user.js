import axios from 'axios';
import { observable } from 'mobx';
import store from 'store';
/**
 * 普通user服务函数，不写样式
 * 用于与后台django交互
 */

store.addPlugin(require('store/plugins/expire'))
/**store需要导入过期插件 */

class UserService{
    @observable loggedin = false;
    @observable errm = true;
    /**mobx模块，定义可观察对象，也就是被观察对象 */
    
    loggedinuser = {
        userid:0,
        username:'',
        mail:'',
        logdate:new Date()
    }

    login(mail,password){
        //TODO 从view层发送来的邮箱和密码，转发给后台服务器
        console.log('class UserService')
        console.log(mail)
        console.log(password)
        /**webpack.config.dev.js中定义了api接口
         * 如果需要后端通信交互数据，需要引用 api
         *  proxy: {
            '/api': {
            target: 'http://127.0.0.1:8000',
            changeOrigin: true
            }
         */
        /** 兼容性更好的浏览浏览器可以使用jquery的ajax，原生*/
        /**
         * 本次使用axios异步库，需要import
         */
        axios.post('/api/user/login/', { /**写相对路径 */
            mail: mail,
            password: password
          })
          .then(response => { /**原来function函数，改为箭头函数，避免下方this没有loggedin属性*/
            console.log(1,response);
            console.log(response.data.id,'++++++++++++++',response.data.token);
            store.set('token',response.data.token,new Date().getTime()+(8*3600));
            /** local 持久化 store，添加token，记录过期时间 */
            this.loggedinuser.userid=response.data.id;
            this.loggedinuser.username=response.data.username;
            this.loggedinuser.mail=response.data.mail;
            this.loggedinuser.logdate=new Date();
            this.loggedin = true;
          })
          .catch(error => {
            console.log(2,error);
            this.errm = false;
            this.loggedin = false;
          });
        
    }


    reg(username,mail,password){
        console.log('class UserService---reg')
        console.log(username)
        console.log(mail)
        console.log(password)
        axios.post('/api/user/reg/', { /**写相对路径 */
            username: username,
            mail: mail,
            password: password
          })
          .then(response => { /**原来function函数，改为箭头函数，避免下方this没有loggedin属性*/
            console.log(1,response);
            console.log(response.data,'++++++++++++++');
            store.set('token',response.data.token,new Date().getTime()+(8*3600));
            this.loggedinuser.userid=response.data.id;
            this.loggedinuser.username=response.data.username;
            this.loggedinuser.mail=response.data.mail;
            this.loggedinuser.logdate=new Date()
            this.loggedin = true;
          })
          .catch(error => {
            console.log(2,error);
            this.loggedin = false;
          });
        
    }
}

const userService = new UserService();
export {userService};
