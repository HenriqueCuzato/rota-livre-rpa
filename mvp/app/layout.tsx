import type { Metadata } from 'next';
import './globals.css';
export const metadata:Metadata={title:'Rota Livre | Uma cidade que inclui',description:'Registre barreiras nas calçadas e acompanhe melhorias de acessibilidade.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="pt-BR"><body>{children}</body></html>}
