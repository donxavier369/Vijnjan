import{i as r,s as n}from"./index-BDOFKY0g.js";const o=async(t,e)=>{try{return n(e),(await r.post("meetings/create-meeting/",t)).data}catch(s){return s.response.data}},c=async t=>{try{return(await r.get(`meetings/list-meeting/${t}/`)).data}catch(e){return e.response.data}};export{o as A,c as G};