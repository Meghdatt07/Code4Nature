import './globals.css';
import { Navbar } from '@/components/shared/navbar';
import { Footer } from '@/components/shared/footer';
import { PageTransition } from '@/components/shared/page-transition';
export const metadata={title:'Code4Nature — Rice Climate Intelligence',description:'Rice climate intelligence for methane reduction, water management, digital MRV and carbon economics.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><Navbar/><PageTransition>{children}</PageTransition><Footer/></body></html>}
