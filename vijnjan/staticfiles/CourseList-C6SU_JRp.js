import{j as e,t as h,B as c,r as o,k as f,T as w}from"./index-BDOFKY0g.js";import{G as N,D as v}from"./Course-D0GWv3rA.js";import{T as C}from"./Category-DO0Ix0aI.js";const F=({setModal:a,id:x,CourseDatafetch:u,setLoading:d})=>{const i=async()=>{d(!0),a(!1);try{const l=await h("token-admin-refresh-vini"),t=await C({is_trending:!0},x,l.access);t.success===!0?(c.success(`${t.message}`),u(),d(!1),console.log(t)):c.error(`${t.message}`)}catch(l){console.log(l)}};return e.jsx(e.Fragment,{children:e.jsx("div",{className:"modal",tabIndex:"-1",role:"dialog",style:{display:"block",background:"rgba(102, 54, 255, 0.12)",borderRadius:"16px",boxShadow:"0 4px 30px rgba(0, 0, 0, 0.1)",backdropFilter:"blur(5.8px)",WebkitBackdropFilter:"blur(5.8px)",border:"1px solid rgba(255, 255, 255, 0.26)"},children:e.jsx("div",{class:"modal-dialog",role:"document",children:e.jsx("div",{class:"modal-content",style:{display:"block",background:"rgba(102, 54, 255, 0.12)",borderRadius:"16px",boxShadow:"0 4px 30px rgba(0, 0, 0, 0.1)",backdropFilter:"blur(5.8px)",WebkitBackdropFilter:"blur(5.8px)",border:"1px solid rgba(255, 255, 255, 0.26)"},children:e.jsxs("div",{className:"modal-body",children:[e.jsx("button",{"aria-label":"Close",className:"btn-close","data-bs-dismiss":"modal",type:"button",onClick:()=>a(!1)}),e.jsx("div",{class:"modal-body",children:e.jsx("p",{className:"text-white",children:"Are you sure you want to delete?"})}),e.jsxs("div",{className:"d-flex justify-content-between",children:[e.jsx("a",{onClick:i,class:"btn btn-danger",type:"button",children:"Yes"}),e.jsx("button",{type:"button",class:"btn btn-secondary","aria-label":"Close","data-bs-dismiss":"modal",onClick:()=>a(!1),id:"close-modal",children:"No"})]})]})})})})})},T=()=>{const[a,x]=o.useState([]),[u,d]=o.useState(!0),[i,l]=o.useState(null),[t,p]=o.useState(!1),[g,b]=o.useState(!1),j=async()=>{try{await w("token-admin-access-vini","admin")?console.log("not expired"):(console.log("token -expired"),window.location.href="/admin-login")}catch(s){console.log(s)}};o.useEffect(()=>{j()},[]);const m=async()=>{try{const s=await N();s.success===!0?(console.log(s),x(s.courses),d(!1)):console.log(s,"error")}catch(s){console.log(s)}};o.useEffect(()=>{m()},[]);const k=async()=>{try{const s=await h("token-admin-refresh-vini"),r=await v(i,s.access);r.success===!0?(console.log(r,"success"),b(!1),c.success(`${r.message}`),m()):(c.error(`${r.message}`),console.log(r,"error"))}catch(s){console.log(s),c.error(`${s}`)}};return e.jsxs("div",{children:[e.jsx(f,{}),e.jsxs("section",{className:"course-two  row home",children:[e.jsx("div",{className:"container",children:e.jsxs("div",{className:"row",children:[e.jsxs("div",{className:"section-title text-center",children:[e.jsx("h5",{className:"section-title__tagline",children:"Hai Welcome Admin"}),e.jsx("h3",{className:"section-title__title",children:a.length===0?"No Course Found !!!":"Course List"})]}),u?e.jsx("div",{className:"loader-container",children:e.jsx("div",{className:"loader"})}):a?a.map((s,r)=>s.data?s.data.map((n,y)=>e.jsx("div",{className:"col-xl-4 col-md-6 wow fadeInUp","data-wow-delay":"400ms",children:e.jsx("div",{children:e.jsxs("a",{children:[e.jsx("div",{children:e.jsx("img",{src:n.thumbnail,alt:"eduact",style:{width:"300px",height:"200px"}})}),e.jsxs("div",{className:"course-two__content",children:[e.jsx("h3",{className:"course-two__title",children:e.jsx("a",{children:n.name})}),e.jsx("p",{children:n.description}),n.is_trending!==!0?e.jsx("button",{className:"btn btn-success me-3",onClick:()=>{l(n.id),p(!0)},children:"Add To Trending"}):"",e.jsx("button",{className:"btn btn-danger",onClick:()=>{l(n.id),b(!0)},"data-bs-target":"#deletemodal","data-bs-toggle":"modal",children:"Delete"})]})]})})},y)):e.jsx("h2",{children:"No course Found !!!"})):""]})}),t&&e.jsx(F,{setModal:p,id:i,CourseDatafetch:m,setLoading:d})]}),g&&e.jsx("div",{className:"modal ",tabIndex:"-1",role:"dialog",style:{display:"block",background:"rgba(102, 54, 255, 0.12)",borderRadius:"16px",boxShadow:"0 4px 30px rgba(0, 0, 0, 0.1)",backdropFilter:"blur(10.8px)",WebkitBackdropFilter:"blur(5.8px)",border:"1px solid rgba(255, 255, 255, 0.26)"},children:e.jsx("div",{class:"modal-dialog",role:"document",children:e.jsx("div",{class:"modal-content",style:{display:"block",background:"rgba(102, 54, 255, 0.12)",borderRadius:"16px",boxShadow:"0 4px 30px rgba(0, 0, 0, 0.1)",backdropFilter:"blur(5.8px)",WebkitBackdropFilter:"blur(5.8px)",border:"1px solid rgba(255, 255, 255, 0.26)"},children:e.jsxs("div",{className:"modal-body",children:[e.jsx("button",{"aria-label":"Close",className:"btn-close","data-bs-dismiss":"modal",type:"button",onClick:()=>b(!1)}),e.jsx("div",{class:"modal-body",children:e.jsx("p",{className:"text-white",children:"Are you sure you want to delete?"})}),e.jsxs("div",{className:"d-flex justify-content-between mt-5",children:[e.jsx("button",{type:"button",class:"btn btn-secondary","aria-label":"Close","data-bs-dismiss":"modal",id:"close-modal",onClick:()=>b(!1),children:"No"}),e.jsx("a",{onClick:k,class:"btn btn-danger",type:"button",children:"Yes"})]})]})})})})]})};export{T as default};