export type VideoItem = {
  id: string;
  title: string;
  description: string;
  category: string;
  duration?: string;
  youtubeId?: string;
  src?: string;
  poster?: string;
};

export const HERO_VIDEO: string | undefined = '/videos/rice-field-hero.mp4';
export const HERO_POSTER: string | undefined = undefined;

export const videos: VideoItem[] = [
  {
    id: 'awd-explained',
    category: 'EXPLAINER',
    title: 'Alternate wetting and drying, explained',
    description: 'How controlled dry-down periods cut methane and save irrigation water without hurting yield.',
    duration: '',
    youtubeId: '',
  },
  {
    id: 'farmer-story',
    category: 'FARMER STORY',
    title: 'On the ground: a season of AWD with smallholder farmers',
    description: 'What changes in the field, the pump bill and the paddy bund when water is managed.',
    duration: '',
    youtubeId: '',
  },
  {
    id: 'methane-and-rice',
    category: 'SCIENCE',
    title: 'Why flooded rice fields emit methane',
    description: 'The soil microbiology behind paddy methane and how drying interrupts it.',
    duration: '',
    youtubeId: '',
  },
];

export const isPlayable = (v: VideoItem) => Boolean(v.youtubeId || v.src);
