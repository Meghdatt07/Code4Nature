import Link from 'next/link';
import { ArrowRight } from 'lucide-react';
import { PageFrame } from '@/components/shared/page-frame';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function Page(){
  const items=["Farm boundary and field measurements","Sentinel-1 SAR pathway for spatial evidence","Water and methane-reduction scenario models","Evidence and provenance layer"];
  return <PageFrame eyebrow="TECHNOLOGY" title="Our technology" description="The prototype connects field evidence, remote sensing, models and an MRV workflow.">
    <div className="grid gap-4 md:grid-cols-2">{items.map((item)=><Card key={item}><div className="text-sm leading-7 text-white/60">{item}</div></Card>)}</div>
    <div className="mt-8 flex flex-wrap gap-3">
      <Link href="/simulator"><Button>Run Farm Simulation <ArrowRight size={15}/></Button></Link>
      <Link href="/mrv"><Button variant="outline">Open Digital MRV</Button></Link>
    </div>
  </PageFrame>
}