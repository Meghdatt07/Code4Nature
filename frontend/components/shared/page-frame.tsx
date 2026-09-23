'use client';
import { ReactNode } from 'react';
import { motion } from 'framer-motion';

export function PageFrame({eyebrow,title,description,children}:{eyebrow?:string;title:string;description?:string;children:ReactNode}){
 return <main className="cc-page">
  <header className="cc-page-hero">
   <div className="cc-page-orb"/>
   <div className="cc-container cc-page-hero-inner">
    <motion.div initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{duration:.55}} className="cc-kicker">{eyebrow||'CODE4NATURE'}</motion.div>
    <motion.h1 initial={{opacity:0,y:22}} animate={{opacity:1,y:0}} transition={{duration:.65,delay:.06}}>{title}</motion.h1>
    {description&&<motion.p initial={{opacity:0,y:18}} animate={{opacity:1,y:0}} transition={{duration:.6,delay:.12}}>{description}</motion.p>}
   </div>
  </header>
  <div className="cc-page-body cc-container">{children}</div>
 </main>
}
export function PageKicker({children}:{children:ReactNode}){return <div className="cc-kicker">{children}</div>}
