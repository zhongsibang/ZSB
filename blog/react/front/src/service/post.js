import axios from 'axios';
import { observable } from 'mobx';
import store from 'store';
store.addPlugin(require('store/plugins/expire'))

class PostService {
    @observable msg = '';
    @observable posts = [];
    @observable pageinfo = { page: 1, size: 5, count: 0, pages: 0 }
    @observable t='';
    @observable c='';
    // constructor(props){
    //     this.axios=axios.create({
    //         baseURL : '/api'
    //     })
    // }
    //可以这样定义axios请求，本次不这样做

    getToken() {
        return store.get('token', '');
    }

    pub(title, content) {
        //TODO
        console.log('class PostService')
        console.log(title)
        console.log(content)

        axios.post('/api/post/pub/',  //为post请求添加头，为后端识别，需要先登录才有token
            {
                title: title,
                content: content
            },
            { headers: { 'jwt': this.getToken() } }
        )
            .then(response => { /**原来function函数，改为箭头函数，避免下方this没有loggedin属性*/
                console.log(1, response);
                console.log(response.data.id, '++++++++++++++', response.data.token);
                this.msg = '提交成功！！！！';
            })
            .catch(error => {
                console.log(2, error);
                this.errm = false;
                this.msg = '提交失败哦~~~~~~~~~~~~~~~~'
            });

    }

    list(search) {
        //TODO search就是查询字符串，直接传给后端django
        axios.get('/api/post/' + search
        )
            .then(response => { /**原来function函数，改为箭头函数，避免下方this没有loggedin属性*/
                console.log(1, response);
                console.log(2, response.data.posts, '++++++++++++++');
                console.log(2, response.data.pageinfo, '++++++++++++++');
                this.posts = response.data.posts;
                this.pageinfo = response.data.pageinfo
            })
            .catch(error => {
                console.log(2, error);
                this.errm = false;

            });

    }

    postDetail(id) {
        axios.get('/api/post/' + id
        )
            .then(response => { /**原来function函数，改为箭头函数，避免下方this没有loggedin属性*/
                console.log(1, response);
                console.log(2, response.data.title, '++++++++++++++');
                console.log(2, response.data.content, '++++++++++++++');
                this.t = response.data.title
                this.c = response.data.content
            })
            .catch(error => {
                console.log(2, error);
                this.errm = false;

            });
    }

}

const postService = new PostService();
export { postService }