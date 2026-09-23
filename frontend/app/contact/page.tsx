import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { PageFrame } from '@/components/shared/page-frame';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
export default function Page(){const items=["Pilot a farm-area workflow","Test MRV evidence requirements","Explore agronomy and remote-sensing validation","Discuss project economics and adoption"];return <PageFrame eyebrow="CONTACT" title="Partner with us" description="Use this page as the starting point for pilot, FPO, research or implementation conversations."><div className="grid gap-4 md:grid-cols-2">{items.map((item)=><Card key={item}><div className="text-sm leading-7 text-white/60">{item}</div></Card>)}</div><div className="mt-8 flex flex-wrap gap-3"><Link href="/simulator"><Button>Run Farm Simulation <ArrowRight size={15}/></Button></Link><Link href="/mrv"><Button variant="outline">Open Digital MRV</Button></Link></div></PageFrame>}