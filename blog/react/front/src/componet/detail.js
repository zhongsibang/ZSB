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
import { inject } from '../service/utils'
import { Card, List, message, Form, Input, Button, Radio, Pagination, InputNumber } from 'antd';
import 'antd/es/form/style'
import 'antd/es/input/style'
import 'antd/es/button/style'
import 'antd/es/radio/style'
import 'antd/es/list/style'
//antd 3以上才支持list控件
import 'antd/es/pagination/style'
import 'antd/es/input-number/style'
import 'antd/es/card/style'

import { observable } from 'mobx';


@inject({ service })
@observer
export class Detail extends React.Component {
    constructor(props){
        super(props);
        console.log(props.match.params.id)
        this.props.service.postDetail(props.match.params.id)
        const detailcontent = this.props.service.c
        console.log(this.props.service.t,'++++++++++++++++++++++++----')
    }
    render() {
        const title = this.props.service.t;
        const content = this.props.service.c;
        return (
            <div style={{ background: '#ECECEC', padding: '30px' }}>
                <Card title={title} bordered={false} style={{ width: '100 %' }}>
                <p>{content}</p>
                </Card>
            </div>
        )
    }

}