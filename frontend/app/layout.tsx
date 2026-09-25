import './globals.css'
import { Navbar } from '@/components/shared/navbar'
import { IntroLoader } from '@/components/shared/intro-loader'

export const metadata = {
  title: 'Asterisk Climos | Climate Intelligence for Low-Emission Rice',
  description: 'Field-level rice water-management, methane and climate-value intelligence.',
  icons: {
    icon: '/favicon.svg',
    shortcut: '/favicon.svg',
    apple: '/favicon.svg',
  },
}

export default function RootLayout({children}:{children:React.ReactNode}){
  return <html lang="en"><body><IntroLoader /><Navbar />{children}</body></html>
}
