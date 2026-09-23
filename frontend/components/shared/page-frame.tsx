import { ReactNode } from 'react';
export function PageFrame({eyebrow,title,description,children}:{eyebrow?:string;title:string;description?:string;children:ReactNode}){
 return <main className="cc-page">
  <header className="cc-page-hero"><div className="cc-container"><div className="cc-kicker">{eyebrow||'CODE4NATURE'}</div><h1>{title}</h1>{description&&<p>{description}</p>}</div></header>
  <div className="cc-page-body cc-container">{children}</div>
 </main>
}
export function PageKicker({children}:{children:ReactNode}){return <div className="cc-kicker">{children}</div>}
