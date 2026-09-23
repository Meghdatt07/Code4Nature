import './globals.css';
import { Navbar } from '@/components/shared/navbar';
import { Footer } from '@/components/shared/footer';
import { Disclaimer } from '@/components/shared/disclaimer';
export const metadata={title:'Asterisk Climos — Climate Intelligence for Low-Emission Rice Farming',description:'Interactive prototype for rice water management, methane-reduction simulation, digital MRV and carbon economics.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body><Navbar/><Disclaimer/>{children}<Footer/></body></html>}
