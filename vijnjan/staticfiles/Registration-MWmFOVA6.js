import{r,j as e,L as k,f as q,B as d}from"./index-BDOFKY0g.js";import{b as $}from"./backgroundgif-CQce0_h5.js";import{u as C}from"./index.esm-Bne98N_B.js";function L(){const{register:t,handleSubmit:x,watch:R,formState:{errors:s}}=C(),[o,p]=r.useState(!1),[c,b]=r.useState(""),[m,f]=r.useState(""),[u,v]=r.useState(""),[h,j]=r.useState("");r.useState("");const[N,w]=r.useState("");r.useState("");const[l,y]=r.useState(""),g=a=>{y(a),setValue("role",a,{shouldValidate:!0})};console.log(l,"selected role");const S=()=>{p(!o)},_=async a=>{try{if(l){const i={username:c,email:u,date_of_birth:h,gender:N,password:m,person:l};console.log(i);const n=await q(i);n.success===!0?(d.success(`${n.message}`),console.log("sucess",n,"response data"),setTimeout(()=>{window.location.href="/login"},1e3)):(console.log(n),d.error(`${n.message}`))}else d.error("Please select who you are: Tutor or Student from above")}catch(i){console.log(i)}};return e.jsx("div",{children:e.jsx("div",{id:"login",className:"master",style:{backgroundImage:`url(${$})`,backgroundRepeat:"no-repeat",backgroundSize:"cover",height:"100vh",display:"block",justifyContent:"center",alignItems:"center",overflowY:"scroll"},children:e.jsx("div",{className:"container",children:e.jsx("div",{id:"login-row",className:"row justify-content-center align-items-center",children:e.jsx("div",{id:"login-column",className:"col-md-6",children:e.jsx("div",{id:"login-box",className:"col-md-12",children:e.jsxs("form",{onSubmit:x(_),children:[e.jsx("h3",{className:"text-center text-inf",children:"Register"}),e.jsxs("div",{className:"form-group-horizontal mt-5",children:[e.jsx("div",{className:"form-group",children:e.jsx("button",{type:"button",className:`btn ${l==="student"?"btn-primary":"btn-light"}`,style:{borderRadius:"25px"},onClick:()=>g("student"),children:"Student"})}),e.jsx("div",{className:"form-group",children:e.jsx("button",{type:"button",className:`btn ${l==="tutor"?"btn-primary":"btn-light"}`,style:{borderRadius:"25px"},onClick:()=>g("tutor"),children:"Tutor"})})]}),s.role&&e.jsx("div",{className:"text-danger mt-2",children:s.role.message}),e.jsxs("div",{className:"form-group mb-3",children:[e.jsx("label",{htmlFor:"email",className:"text-inf",children:"Email:"}),e.jsx("br",{}),e.jsx("input",{...t("email",{required:"Email is required",pattern:{value:/^[^\s@]+@[^\s@]+\.[^\s@]+$/,message:"Invalid email address"}}),placeholder:"abcd@gmail.com",className:"form-control",value:u,onChange:a=>v(a.target.value)}),s.email&&e.jsx("p",{className:"text-danger",children:s.email.message})]}),e.jsxs("div",{className:"form-group mb-3",children:[e.jsx("label",{htmlFor:"password",className:"text-inf",children:"Password:"}),e.jsx("br",{}),e.jsxs("div",{className:"input-group",children:[e.jsx("input",{type:o?"text":"password",placeholder:"password",className:`form-control ${s.password?"is-invalid":""}`,...t("password",{required:"Password is required",minLength:{value:8,message:"Password must be at least 8 characters long"},pattern:{value:/(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])/,message:"Password must contain at least one number, one lowercase and one uppercase letter"}}),value:m,onChange:a=>f(a.target.value)}),e.jsx("div",{className:"input-group-append",children:e.jsx("button",{className:"btn btn-light mx-1",type:"button",style:{border:"1px solid #000"},onClick:S,children:e.jsx("i",{id:"passwordIcon",className:o?"fas fa-eye":"fas fa-eye-slash"})})}),s.password&&e.jsx("div",{className:"invalid-feedback",children:s.password.message})]})]}),e.jsxs("div",{className:"form-group mb-3",children:[e.jsx("label",{htmlFor:"username",className:"text-inf",children:"Username:"}),e.jsx("br",{}),e.jsx("input",{type:"text",placeholder:"username",className:`form-control ${s.username?"is-invalid":""}`,...t("username",{required:"Username is required",maxLength:{value:20,message:"Username cannot exceed 20 characters"},minLength:{value:3,message:"Username must have been minimum 3 Character required"},pattern:{value:/^[a-zA-Z0-9]*$/,message:"Username can only contain letters and numbers"}}),value:c,onChange:a=>b(a.target.value)}),s.username&&e.jsx("div",{className:"invalid-feedback",children:s.username.message})]}),e.jsxs("div",{className:"form-group-horizontal",children:[e.jsxs("div",{className:"form-group mb-3",children:[e.jsx("label",{htmlFor:"date_of_birth",className:"text-inf",children:"Date of Birth:"}),e.jsx("br",{}),e.jsx("input",{type:"date",name:"date_of_birth",id:"date_of_birth",className:`form-control ${s.date_of_birth?"is-invalid":""}`,...t("date_of_birth",{required:"Date of Birth is required"}),value:h,onChange:a=>j(a.target.value)}),s.date_of_birth&&e.jsx("div",{className:"invalid-feedback",children:s.date_of_birth.message})]}),e.jsxs("div",{className:"form-group",children:[e.jsx("label",{htmlFor:"gender",className:"text-inf",children:"Gender:"}),e.jsx("br",{}),e.jsxs("select",{id:"gender",className:`form-control ${s.gender?"is-invalid":""}`,...t("gender",{required:"Gender is required"}),style:{height:"40px",width:"100%",borderRadius:"10px"},onChange:a=>w(a.target.value),children:[e.jsx("option",{value:"",children:"Select gender"}),e.jsx("option",{value:"male",children:"Male"}),e.jsx("option",{value:"female",children:"Female"})]}),s.gender&&e.jsx("div",{className:"invalid-feedback",children:s.gender.message})]})]}),e.jsx("div",{className:"form-group mb-3 mt-3",children:e.jsx("button",{type:"submit",className:"btn btn-primary",children:"Sign up"})}),e.jsxs("div",{className:"form-group mb-3",children:[e.jsx("label",{htmlFor:"password",className:"text-inf"}),e.jsx("br",{}),e.jsx(k,{to:"/login",style:{color:"#fff"},children:"if you already have an account please Login !!!"})]})]})})})})})})})}export{L as default};