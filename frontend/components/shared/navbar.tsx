'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { ChevronDown, Menu, X } from 'lucide-react';
import { useState } from 'react';

const navigation = [
  ['Home', '/'],
  ['Rice carbon credits', '/rice-carbon-credits'],
  ['Climate-smart rice', '/climate-smart-rice'],
  ['Our technology', '/technology'],
  ['Farm simulator', '/simulator'],
  ['Carbon economics', '/carbon'],
  ['Digital MRV', '/mrv'],
  ['Research', '/research'],
  ['Insights', '/insights'],
  ['News', '/news'],
  ['Industry', '/industry'],
  ['Partner with us', '/partner-with-us'],
  ['About', '/about'],
  ['Contact', '/contact'],
];

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  const active = (href: string) =>
    href === '/' ? pathname === '/' : pathname === href || pathname.startsWith(href + '/');

  return (
    <nav className="site-nav">
      <div className="nav-announcement">
        Rice methane + water intelligence ·{' '}
        <Link href="/technology">Explore the Asterisk Climos technology →</Link>
      </div>

      <div className="nav-inner">
        <Link href="/" className="brand" aria-label="Asterisk Climos home" onClick={() => setOpen(false)}>
          <img className="brand-logo brand-logo-dark" src="/logo-dark.svg" alt="Asterisk Climos" />
          <img className="brand-logo brand-logo-light" src="/logo-light.svg" alt="Asterisk Climos" />
        </Link>

        <div className="nav-spacer" />

        <div className="nav-menu-wrap">
          <button
            type="button"
            className={`nav-menu-button${open ? ' open' : ''}`}
            aria-expanded={open}
            aria-haspopup="menu"
            onClick={() => setOpen((value) => !value)}
          >
            <Menu size={18} />
            <span>Menu</span>
            <ChevronDown size={14} className="nav-menu-chevron" />
          </button>

          {open && (
            <div className="nav-menu-panel" role="menu">
              <div className="nav-menu-heading">Explore Asterisk Climos</div>
              <div className="nav-menu-grid">
                {navigation.map(([label, href]) => (
                  <Link
                    key={href}
                    href={href}
                    role="menuitem"
                    className={`nav-menu-link${active(href) ? ' active' : ''}`}
                    onClick={() => setOpen(false)}
                  >
                    <span>{label}</span>
                    {active(href) && <span className="nav-menu-current">Current</span>}
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>

        <button
          className="mobile-menu"
          aria-label={open ? 'Close navigation' : 'Open navigation'}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="mobile-panel">
          <div className="mobile-panel-heading">Explore Asterisk Climos</div>
          {navigation.map(([label, href]) => (
            <Link key={href} href={href} onClick={() => setOpen(false)}>
              {label}
              {active(href) && <span className="nav-menu-current">Current</span>}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
