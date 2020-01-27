import React from 'react';

//装饰器，为函数动态曾加service属性
//const inject = obj => Comp => props =><Comp {...obj}/> ;
const inject = obj => Comp => props =><Comp {...obj} {...props} /> ;
export {inject};