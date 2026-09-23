'use client';
import { useState } from 'react';
import { ChevronDown } from 'lucide-react';
export function AccordionList({ items }: { items: { title: string; body: string }[] }) {
  const [open, setOpen] = useState(0);
  return <div className="space-y-3">{items.map((item, i) => (
    <div key={item.title} className="rounded-2xl border border-white/10 bg-white/[0.03]">
      <button className="flex w-full items-center justify-between gap-4 p-5 text-left" onClick={() => setOpen(open === i ? -1 : i)} aria-expanded={open === i}>
        <span className="font-semibold">{item.title}</span><ChevronDown size={18} className={`transition ${open === i ? 'rotate-180' : ''}`} />
      </button>
      {open === i && <div className="border-t border-white/5 px-5 pb-5 pt-4 text-sm leading-7 text-white/55">{item.body}</div>}
    </div>
  ))}</div>;
}