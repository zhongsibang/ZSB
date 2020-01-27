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
import { List, message, Form, Input, Button, Radio, Pagination, InputNumber } from 'antd';
import 'antd/es/form/style'
import 'antd/es/input/style'
import 'antd/es/button/style'
import 'antd/es/radio/style'
import 'antd/es/list/style'
//antd 3以上才支持list控件
import 'antd/es/pagination/style'
import 'antd/es/input-number/style'

import { observable } from 'mobx';

@inject({service})
@observer
export class Llist extends React.Component {
  constructor(props) {
    super(props);
    //let {search} = this.props.location
    console.log('.............',props.location.search)//获取查询字符串
    // 前端路由一定要使用<Route path="/list" component={Llist} />
    //路由相关信息，包括路径，查询字符串等等才会传入Llist的props中
    console.log('.............')
    this.props.service.list(props.location.search)
  }

  handleOnchange(page, pageSize){
    console.log(page, pageSize)
    this.props.service.list('?page='+page+'&size='+pageSize)
  }

  sizeChange(number){
    this.props.service.list('?size='+number)
  }

  render() {
    const data = this.props.service.posts;
    const {count,page,pages,size} = this.props.service.pageinfo
    //console.log(count,page,pages,size,'++++++++++++++++++++++')
    return (
      <List
        header={<div>
          博客列表
          Size:<InputNumber defaultValue={size} onChange={this.sizeChange.bind(this)} />
        </div>}
        footer={<div>
          <Pagination 
          current={page} 
          total={count}
          pageSize={size}
          onChange={this.handleOnchange.bind(this)}
          /></div>}
        bordered
        dataSource={data}
    renderItem={item => (<List.Item><Link to={'/post/'+item.post_id}>{item.post_title}</Link> {item.post_date}</List.Item>)}
      />);
  }
}


// import { InputNumber } from 'antd';

// function onChange(value) {
//   console.log('changed', value);
// }

// ReactDOM.render(<InputNumber min={1} max={10} defaultValue={3} onChange={onChange} />, mountNode);