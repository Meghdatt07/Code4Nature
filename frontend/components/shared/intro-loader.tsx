'use client'

import { useEffect, useState } from 'react'

export function IntroLoader(){
  const [ready,setReady]=useState(false)

  useEffect(()=>{
    document.body.classList.add('intro-lock')
    const timer=window.setTimeout(()=>setReady(true),4200)
    return ()=>window.clearTimeout(timer)
  },[])

  const enter=()=>{
    if(!ready)return
    document.body.classList.remove('intro-lock')
    document.documentElement.classList.add('intro-entering')
    window.setTimeout(()=>{
      document.documentElement.classList.remove('intro-entering')
      const el=document.getElementById('siteIntro')
      el?.remove()
    },650)
  }

  return <div id="siteIntro" className="site-intro" aria-label="Asterisk Climos introduction">
    <svg className="intro-hero-art" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
      <defs>
        <linearGradient id="introSky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#10272b"/><stop offset=".42" stopColor="#355b50"/><stop offset="1" stopColor="#111f18"/>
        </linearGradient>
        <linearGradient id="introWater" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#91d8d6" stopOpacity=".88"/><stop offset=".32" stopColor="#2a8880" stopOpacity=".8"/><stop offset="1" stopColor="#073b36" stopOpacity=".97"/>
        </linearGradient>
        <linearGradient id="introDry" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#8e754c"/><stop offset=".45" stopColor="#5b3e24"/><stop offset="1" stopColor="#21150c"/>
        </linearGradient>
        <linearGradient id="introLeaf" x1="0" y1="1" x2="1" y2="0">
          <stop offset="0" stopColor="#2e6f39"/><stop offset=".58" stopColor="#77bd52"/><stop offset="1" stopColor="#d3ef7c"/>
        </linearGradient>
        <linearGradient id="introRoot" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#ecd7ae"/><stop offset="1" stopColor="#83542d"/>
        </linearGradient>
        <radialGradient id="introSun">
          <stop stopColor="#fff6cc" stopOpacity=".95"/><stop offset=".26" stopColor="#ffd87c" stopOpacity=".52"/><stop offset="1" stopColor="#ffd87c" stopOpacity="0"/>
        </radialGradient>
        <linearGradient id="introVignette" x1="0" y1="0" x2="0" y2="1">
          <stop stopColor="#000" stopOpacity=".15"/><stop offset=".5" stopColor="#000" stopOpacity="0"/><stop offset="1" stopColor="#000" stopOpacity=".58"/>
        </linearGradient>
        <filter id="introBlur"><feGaussianBlur stdDeviation="16"/></filter>
        <filter id="introGlow"><feGaussianBlur stdDeviation="5"/></filter>
      </defs>

      <rect width="1600" height="900" fill="url(#introSky)"/>
      <circle cx="1370" cy="155" r="190" fill="url(#introSun)" filter="url(#introGlow)"/>
      <circle cx="1370" cy="155" r="35" fill="#ffe9ab" opacity=".86"/>

      <path d="M0 270 Q160 200 330 245 T680 230 T1010 250 T1330 225 T1600 240 V510 H0Z" fill="#294e45"/>
      <path d="M0 315 Q190 250 410 292 T820 282 T1230 305 T1600 275 V510 H0Z" fill="#476b5c" opacity=".78"/>
      <path d="M0 365 Q210 315 460 354 T930 346 T1330 362 T1600 350 V510 H0Z" fill="#79927a" opacity=".45"/>
      <rect y="404" width="1600" height="105" fill="#dbe9dd" opacity=".08" filter="url(#introBlur)"/>

      {/* flooded half */}
      <rect x="0" y="500" width="800" height="230" fill="url(#introWater)"/>
      <path d="M0 504 Q170 485 335 504 T650 498 T800 505" fill="none" stroke="#e7ffff" strokeOpacity=".58" strokeWidth="4"/>
      <path d="M0 535 Q160 519 330 537 T650 532 T800 539" fill="none" stroke="#c9fffb" strokeOpacity=".2" strokeWidth="2"/>
      <rect x="0" y="730" width="800" height="170" fill="#2e1e12"/>

      {/* dry half */}
      <rect x="800" y="536" width="800" height="364" fill="url(#introDry)"/>
      <path d="M800 553 Q950 522 1090 548 T1370 542 T1600 554" fill="none" stroke="#e1b273" strokeOpacity=".35" strokeWidth="4"/>
      <path d="M850 635 Q950 600 1050 640 T1260 630 T1450 645 T1600 625" fill="none" stroke="#d39b5c" strokeOpacity=".18" strokeWidth="5"/>

      {/* flooded rice */}
      <g>
        <path d="M400 730 C408 650 408 566 402 505" fill="none" stroke="#7b9a57" strokeWidth="14" strokeLinecap="round"/>
        <path d="M402 520 C305 420 260 345 285 240 C360 310 401 406 402 520Z" fill="url(#introLeaf)"/>
        <path d="M405 520 C516 429 567 345 550 225 C470 304 427 405 405 520Z" fill="url(#introLeaf)"/>
        <path d="M406 545 C314 485 232 467 138 471 C217 538 308 577 406 545Z" fill="url(#introLeaf)"/>
        <path d="M410 561 C508 500 590 486 674 512 C598 576 503 588 410 561Z" fill="url(#introLeaf)"/>
      </g>

      {/* dry rice */}
      <g>
        <path d="M1197 738 C1202 654 1194 566 1195 514" fill="none" stroke="#708d50" strokeWidth="14" strokeLinecap="round"/>
        <path d="M1195 524 C1099 424 1065 338 1097 238 C1160 320 1192 418 1195 524Z" fill="url(#introLeaf)"/>
        <path d="M1197 526 C1292 427 1372 346 1450 307 C1401 418 1312 502 1197 526Z" fill="url(#introLeaf)"/>
        <path d="M1195 554 C1097 496 1019 482 930 500 C1005 560 1096 580 1195 554Z" fill="url(#introLeaf)"/>
        <path d="M1198 572 C1296 519 1397 518 1494 553 C1402 607 1297 608 1198 572Z" fill="url(#introLeaf)"/>
      </g>

      {/* roots */}
      <g fill="none" stroke="url(#introRoot)" strokeLinecap="round">
        <path d="M400 714 C366 764 342 816 320 872 M404 712 C405 775 392 836 376 895 M407 714 C450 763 477 822 495 880 M398 723 C350 760 305 776 260 790 M411 730 C460 757 510 780 557 792" strokeWidth="6"/>
        <path d="M1194 720 C1154 768 1134 822 1112 884 M1196 719 C1193 780 1185 840 1172 895 M1200 720 C1240 766 1274 821 1304 874 M1204 723 C1254 753 1305 771 1354 783" strokeWidth="6"/>
      </g>

      {/* methane bubbles */}
      <g fill="#efffff" fillOpacity=".06" stroke="#e7ffff" strokeOpacity=".62">
        <circle cx="115" cy="610" r="22"/><circle cx="190" cy="662" r="36"/><circle cx="276" cy="588" r="19"/><circle cx="340" cy="675" r="29"/>
        <circle cx="438" cy="622" r="17"/><circle cx="510" cy="694" r="33"/><circle cx="610" cy="610" r="21"/><circle cx="684" cy="658" r="14"/>
        <circle cx="246" cy="755" r="16"/><circle cx="734" cy="573" r="10"/>
        <circle cx="1364" cy="696" r="19"/><circle cx="1452" cy="773" r="13"/><circle cx="1280" cy="807" r="11"/><circle cx="1512" cy="653" r="8"/>
      </g>
      <g fill="#fff" opacity=".78">
        <circle cx="107" cy="603" r="3"/><circle cx="177" cy="649" r="4"/><circle cx="330" cy="665" r="3"/><circle cx="500" cy="681" r="4"/><circle cx="600" cy="602" r="3"/><circle cx="1357" cy="689" r="3"/>
      </g>

      <rect width="1600" height="900" fill="url(#introVignette)"/>
    </svg>

    <div className="intro-ui" aria-hidden="false">
      <div className="intro-brand">✦ &nbsp; ASTERISK CLIMOS &nbsp; · &nbsp; CODE4NATURE</div>

      <div className="intro-field-label intro-field-label-left">
        <strong>FLOODED FIELD</strong><span>CONTINUOUS SUBMERGENCE</span>
        <em>↑ HIGHER CH₄</em><small>Anaerobic soil conditions increase methane emissions</small>
      </div>
      <div className="intro-field-label intro-field-label-right">
        <strong>AWD / DRY-DOWN</strong><span>INTERMITTENT IRRIGATION</span>
        <em>↓ LOWER CH₄</em><small>Periodic drying reduces methane emissions</small>
      </div>

      <div className="intro-bottom">
        <div className="intro-welcome">WELCOME TO THE WORLD OF OPPORTUNITIES</div>
        <h1>ASTERISK <span>CLIMOS</span></h1>
        <div className="intro-subtitle">MEASURE · OPTIMIZE · REDUCE · CREATE VALUE</div>
        <div className="intro-progress"><span className={ready?'is-ready':''}/></div>
        <div className="intro-loading">LOADING CLIMATE INTELLIGENCE… <b>{ready?'100%':'CALIBRATING'}</b></div>
        <button id="introEnter" type="button" disabled={!ready} onClick={enter} className={ready?'is-ready':''}>LET’S GO ↗</button>
      </div>
    </div>
  </div>
}