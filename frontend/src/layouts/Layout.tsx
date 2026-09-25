
  import { ReactNode } from 'react';
  import Sidebar from '../components/Sidebar';
  import Header from '../components/Header';

  interface LayoutProps {
    children: ReactNode;
  }

  export default function Layout({ children }: LayoutProps) {
    return (
      <div className="min-h-screen bg-[#F0F4F8] flex">
        <Sidebar />
        <div className="flex-1 ml-64 flex flex-col min-h-screen">
          <Header />
          <main className="flex-1 p-8 overflow-y-auto">
            <div className="max-w-7xl mx-auto">
              {children}
            </div>
          </main>
        </div>
      </div>
    );
  }