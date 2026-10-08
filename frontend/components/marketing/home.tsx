'use client';

import { useState } from 'react';
import { Play, Satellite, MapPinned, Gauge, Radio, Check, CircleDot } from 'lucide-react';
import { EvidenceVisual, Reveal } from '@/components/marketing/marketing';
import { VideoItem, isPlayable, videos } from '@/lib/videos';

export function HeroBackdrop({ src, poster }: { src?: string; poster?: string }) {
  const [failed, setFailed] = useState(false);
  const [ready, setReady] = useState(false);
  return <div className="hv-backdrop" aria-hidden="true">
    <PaddyScene />
    {src && !failed && <video className={`hv-bg-video${ready ? ' is-ready' : ''}`} autoPlay muted loop playsInline preload="metadata" poster={poster} onLoadedData={() => setReady(true)}><source src={src} type="video/mp4" onError={() => setFailed(true)} /></video>}
    <div className="hv-backdrop-shade" />
  </div>;
}

export function PaddyScene() {
  return <svg className="hv-scene" viewBox="0 0 1440 800" preserveAspectRatio="xMidYMid slice">
    <defs>
      <linearGradient id="hv-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#081f19" /><stop offset=".5" stopColor="#25594a" /><stop offset="1" stopColor="#d8c98c" /></linearGradient>
      <linearGradient id="hv-water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#7fb3c4" /><stop offset="1" stopColor="#2c6b78" /></linearGradient>
      <linearGradient id="hv-green1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#5fa564" /><stop offset="1" stopColor="#2f7447" /></linearGradient>
      <linearGradient id="hv-green2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#3d8a52" /><stop offset="1" stopColor="#1f5a38" /></linearGradient>
      <pattern id="hv-rows" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M8 16V5M8 9 5 6M8 9l3-3" stroke="#b9e59a" strokeOpacity=".45" strokeWidth="1.2" fill="none" /></pattern>
    </defs>
    <rect width="1440" height="800" fill="url(#hv-sky)" />
    <circle className="hv-sun" cx="1090" cy="310" r="74" fill="#f7e9ab" /><circle cx="1090" cy="310" r="150" fill="#f7e9ab" opacity=".1" />
    <path d="M0 430C180 360 340 410 520 372C700 336 860 410 1040 366C1220 330 1340 392 1440 356V800H0Z" fill="#17463a" opacity=".85" />
    <path d="M0 470C180 410 340 450 520 420C700 392 860 446 1040 410C1220 380 1340 428 1440 402V800H0Z" fill="#1d5442" />
    <path d="M0 525C240 485 480 545 720 508C960 472 1200 532 1440 498V800H0Z" fill="url(#hv-water)" />
    <ellipse className="hv-glint g1" cx="300" cy="545" rx="110" ry="5" fill="#fff" opacity=".35" /><ellipse className="hv-glint g2" cx="820" cy="530" rx="140" ry="5" fill="#fff" opacity=".3" /><ellipse className="hv-glint g3" cx="1180" cy="520" rx="90" ry="4" fill="#fff" opacity=".3" />
    <path d="M0 606C260 566 520 630 800 590C1060 552 1260 604 1440 578V800H0Z" fill="url(#hv-green1)" /><path d="M0 606C260 566 520 630 800 590C1060 552 1260 604 1440 578V800H0Z" fill="url(#hv-rows)" />
    <path d="M0 694C300 654 600 718 900 678C1160 644 1320 694 1440 668V800H0Z" fill="url(#hv-green2)" /><path d="M0 694C300 654 600 718 900 678C1160 644 1320 694 1440 668V800H0Z" fill="url(#hv-rows)" />
    <path d="M0 764C360 730 760 792 1100 754C1260 738 1380 754 1440 748V800H0Z" fill="#14402a" />
  </svg>;
}

export function VideoCard({ video, featured = false }: { video: VideoItem; featured?: boolean }) {
  const [playing, setPlaying] = useState(false);
  const playable = isPlayable(video);
  const thumb = video.poster ?? (video.youtubeId ? `https://i.ytimg.com/vi/${video.youtubeId}/hqdefault.jpg` : undefined);
  return <figure className={`hv-video${featured ? ' hv-video-featured' : ''}${playable ? '' : ' is-placeholder'}`}>
    <div className="hv-video-frame">
      {playing && playable ? (
        video.youtubeId ? <iframe src={`https://www.youtube-nocookie.com/embed/${video.youtubeId}?autoplay=1&rel=0&modestbranding=1&playsinline=1`} title={video.title} allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowFullScreen /> : <video src={video.src} poster={video.poster} controls autoPlay playsInline />
      ) : <button type="button" className="hv-video-poster" disabled={!playable} onClick={() => setPlaying(true)} aria-label={playable ? `Play video: ${video.title}` : `Video placeholder: ${video.title}`}>
        {thumb && <img src={thumb} alt="" loading="lazy" />}
        <span className="hv-video-tag">{video.category}</span>
        <span className="hv-play"><Play size={featured ? 30 : 22} fill="currentColor" /></span>
        {video.duration && <span className="hv-video-duration">{video.duration}</span>}
        {!playable && <span className="hv-video-todo">Add a YouTube ID or local src in lib/videos.ts</span>}
      </button>}
    </div>
    <figcaption><h3>{video.title}</h3><p>{video.description}</p></figcaption>
  </figure>;
}

export function VideoGallery() {
  const dev = process.env.NODE_ENV !== 'production';
  const list = dev ? videos : videos.filter(isPlayable);
  if (list.length === 0) return null;
  const [first, ...rest] = list;
  return <div className="hv-video-grid"><Reveal className="hv-video-main"><VideoCard video={first} featured /></Reveal><div className="hv-video-side">{rest.map((v, i) => <Reveal key={v.id} delay={0.08 * (i + 1)}><VideoCard video={v} /></Reveal>)}</div></div>;
}

const techTabs = [
  { key: 'assess', label: 'Assess project area', icon: MapPinned, title: 'Know where AWD can work.', copy: 'Map field boundaries, crop calendars and irrigation conditions to understand where controlled dry-down is feasible, and where it is not. AWD is not recommended in rainfed systems with uncertain water supply.' },
  { key: 'monitor', label: 'Monitor practice adoption', icon: Satellite, title: 'See the practice, field by field.', copy: 'Sentinel-1 SAR can pick up flooding and drying through cloud cover. Combined with farmer logs and field visits, it shows whether a dry-down actually happened.' },
  { key: 'measure', label: 'Measure real impact', icon: Gauge, title: 'Turn evidence into a defensible number.', copy: 'Process-based models, calibrated against direct methane measurements where available, estimate avoided emissions with an explicit uncertainty deduction.' },
] as const;

export function TechTabs() {
  const [active, setActive] = useState<(typeof techTabs)[number]['key']>('assess');
  const tab = techTabs.find((t) => t.key === active)!;
  return <div className="hv-tech">
    <div className="hv-tech-tabs" role="tablist">
      {techTabs.map((t) => { const Icon = t.icon; return <button key={t.key} role="tab" aria-selected={t.key === active} className={t.key === active ? 'is-active' : ''} onClick={() => setActive(t.key)}><Icon size={18} /><span>{t.label}</span></button>; })}
    </div>
    <div className="hv-tech-body"><div key={tab.key} className="hv-tech-copy"><h3>{tab.title}</h3><p>{tab.copy}</p></div><EvidenceVisual /></div>
  </div>;
}
