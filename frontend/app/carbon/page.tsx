import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { PageFrame } from '@/components/shared/page-frame';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
export default function Page(){const items=["Change project area and emissions assumptions.","Compare a stable ERF-style scenario with a market proxy.","Adjust farmer/FPO share and inspect gross value."];return <PageFrame eyebrow="ECONOMICS" title="Carbon economics" description="Model carbon price scenarios and revenue allocation for farmers/FPOs and the MRV platform."><div className="grid gap-4 md:grid-cols-2">{items.map((item)=><Card key={item}><div className="text-sm leading-7 text-white/60">{item}</div></Card>)}</div><div className="mt-8 flex flex-wrap gap-3"><Link href="/simulator"><Button>Run Farm Simulation <ArrowRight size={15}/></Button></Link><Link href="/mrv"><Button variant="outline">Open Digital MRV</Button></Link></div></PageFrame>}