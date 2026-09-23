import './globals.css';
import { Navbar } from '@/components/shared/navbar';
import { Footer } from '@/components/shared/footer';
import { Disclaimer } from '@/components/shared/disclaimer';

export const metadata={
 title:'Code4Nature — Rice Climate Intelligence',
 description:'Field-level intelligence for climate-smart rice, methane reduction, digital MRV and carbon economics.'
};

export default function RootLayout({children}:{children:React.ReactNode}){
 return <html lang="en"><body><Navbar/><Disclaimer/>{children}<Footer/></body></html>
}
