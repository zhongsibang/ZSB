import React from 'react';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
  } from "react-router-dom";
import { postService as service } from '../service/post';
import { observer } from 'mobx-react';
import 'antd/es/message/style'
//import { func } from 'prop-types';
import { inject } from '../service/utils'
import { message, Form, Input, Button, Radio } from 'antd';
import 'antd/es/form/style'
import 'antd/es/input/style'
import 'antd/es/button/style'
import 'antd/es/radio/style'
import 'antd/es/message/style'

const { TextArea } = Input;

@inject({service}) //内部参数是数组service=service
@observer
export default class Pub extends React.Component{
    handleSubmit(event){
        event.preventDefault();
        const [title,content] = event.target
        this.props.service.pub(title.value,content.value)
        // console.log(event.target[0].value)
        // console.log(event.target[1].value) 
        //注意和login、reg获取方式不一样，pub是form提交，login reg 是botton提交
    }


    render(){
        let em =this.props.service.msg
        return( // onSubmit={this.handleSubmit.bind(this)}  一定要绑定this
            <div>
                <Form layout="horizontal" onSubmit={this.handleSubmit.bind(this)} > 
                    <Form.Item label="Title">
                        <Input placeholder="Title Here!!!" />
                    </Form.Item>
                    <Form.Item label="Content:">
                        <TextArea placeholder="Content Here!!!" rows={10} />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" htmlType="submit">提交</Button>
                    </Form.Item>
                </Form>
            </div>
        )
    }

    componentDidUpdate(preProps,preState){
        if (preProps.service.msg) {
              message.info(preProps.service.msg, 5,()=>preProps.service.msg='');
        }
    } 
}
