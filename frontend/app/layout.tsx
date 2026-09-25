import './globals.css'
import { Navbar } from '@/components/shared/navbar'

export const metadata = {
  title: 'Code4Nature | Climate Intelligence for Low-Emission Rice',
  description: 'Field-level rice water-management, methane and climate-value intelligence.'
}

export default function RootLayout({children}:{children:React.ReactNode}){
  return <html lang="en"><body><Navbar />{children}</body></html>
}
