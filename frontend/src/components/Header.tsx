import { useState, useEffect } from 'react';
  import { useLocation } from 'react-router-dom';

  export default function Header() {
    const [time, setTime] = useState(new Date().toLocaleTimeString());
    const location = useLocation();

    useEffect(() => {
      const timer = setInterval(() => {
        setTime(new Date().toLocaleTimeString());
      }, 1000);
      return () => clearInterval(timer);
    }, []);

    const getPageTitle = () => {
      const path = location.pathname;
      if (path === '/') return 'Dashboard';
      if (path.startsWith('/machines/')) return 'Machine Details';
      if (path.startsWith('/machines')) return 'Machines';
      if (path.startsWith('/maintenance')) return 'Maintenance';
      if (path.startsWith('/test-prediction')) return 'Test Prediction';
      if (path.startsWith('/reports')) return 'Reports';
      return 'Dashboard';
    };

    return (
      <header className="bg-white border-b border-[#E2E8F0] h-16 sticky top-0 z-10 shadow-sm">
        <div className="flex items-center justify-between px-8 h-full">
          <div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-[#0F172A]
  to-[#3B82F6]">
              {getPageTitle()}
            </h1>
          </div>

          <div className="flex items-center gap-6">
            <div className="flex items-center gap-3 bg-[#F8FAFC] px-4 py-2 rounded-lg border
  border-[#E2E8F0]">
              <span className="text-lg">🕒</span>
              <span className="font-mono-data text-sm font-semibold text-[#1E293B] min-w-[85px]">
                {time}
              </span>
            </div>
          </div>
        </div>
      </header>
    );
  }