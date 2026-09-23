'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState } from 'react';
import { ChevronDown, Menu, X } from 'lucide-react';
import { Button } from '@/components/ui/button';

const primary=[['Rice carbon credits','/rice-carbon-credits'],['Climate-smart rice','/climate-smart-rice'],['Our technology','/technology']];
const more=[['Farm simulator','/simulator'],['Digital MRV','/mrv'],['Carbon economics','/carbon'],['Research','/research'],['Insights','/insights'],['Industry','/industry'],['About','/about']];
export function Navbar(){
 const pathname=usePathname(); const [open,setOpen]=useState(false);
 const active=(p:string)=>pathname===p||pathname.startsWith(p+'/');
 return <nav className="site-nav">
  <div className="nav-inner">
   <Link href="/" className="brand" onClick={()=>setOpen(false)}>CODE<span>4</span>NATURE</Link>
   <div className="desktop-nav">
    {primary.map(([label,href])=><Link key={href} href={href} className={active(href)?'active':''}>{label}</Link>)}
    <div className="nav-more">
      <button>Explore <ChevronDown size={14}/></button>
      <div className="nav-menu">{more.map(([label,href])=><Link key={href} href={href}>{label}</Link>)}</div>
    </div>
    <Link href="/contact" className="nav-cta">Partner with us <ArrowIcon/></Link>
   </div>
   <button className="mobile-menu" aria-label="Open navigation" onClick={()=>setOpen(v=>!v)}>{open?<X/>:<Menu/>}</button>
  </div>
  {open&&<div className="mobile-panel">{[...primary,...more,['Partner with us','/contact']].map(([label,href])=><Link key={href} href={href} onClick={()=>setOpen(false)}>{label}<ArrowIcon/></Link>)}</div>}
 </nav>
}
function ArrowIcon(){return <span className="nav-arrow">↗</span>}
