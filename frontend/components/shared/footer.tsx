import Link from 'next/link';
export function Footer(){
 return <footer className="site-footer">
  <div className="footer-top cc-container">
   <div><Link href="/" className="footer-brand">CODE<span>4</span>NATURE</Link><p>Climate intelligence for rice farming. Measuring water, methane and carbon value through field-level data.</p></div>
   <div><small>EXPLORE</small><Link href="/climate-smart-rice">Climate-smart rice</Link><Link href="/technology">Our technology</Link><Link href="/simulator">Farm simulator</Link><Link href="/mrv">Digital MRV</Link></div>
   <div><small>CLIMATE VALUE</small><Link href="/rice-carbon-credits">Rice carbon credits</Link><Link href="/carbon">Carbon economics</Link><Link href="/research">Science & research</Link><Link href="/contact">Partner with us</Link></div>
  </div>
  <div className="footer-bottom cc-container"><span>© {new Date().getFullYear()} Code4Nature</span><span>Built around evidence • designed for action</span></div>
 </footer>
}
