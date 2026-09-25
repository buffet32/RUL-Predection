
import { Link, useLocation } from 'react-router-dom';

  interface NavItem {
    name: string;
    href: string;
    icon: string;
  }

  const navigation: NavItem[] = [
    { name: 'Dashboard', href: '/', icon: '📊' },
    { name: 'Machines', href: '/machines', icon: '⚙️  ' },
    { name: 'Maintenance', href: '/maintenance', icon: '🔧' },
    { name: 'Test Prediction', href: '/test-prediction', icon: '🧪' },
    { name: 'Reports', href: '/reports', icon: '📈' },
    { name: 'Data Quality', href: '/data-quality', icon: '✅' },
  ];

  export default function Sidebar() {
    const location = useLocation();

    return (
      <div className="flex flex-col h-full bg-gradient-to-b from-[#0F172A] to-[#1E293B] border-r
  border-[#334155]">
        {/* Logo Section */}
        <div className="px-6 py-6 border-b border-[#334155]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-[#667EEA] to-[#764BA2] rounded-xl flex
  items-center justify-center shadow-lg">
              <span className="text-2xl">🏭</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-white">PdM System</h1>
              <p className="text-xs text-[#94A3B8]">Predictive Maintenance</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center gap-3 px-4 py-3 text-sm font-medium rounded-xl transition-all duration-300 group ${
                  isActive
                    ? 'bg-gradient-to-r from-[#667EEA] to-[#764BA2] text-white shadow-md transform translate-x-1'
                    : 'text-[#94A3B8] hover:bg-[#1E3A5F] hover:text-white hover:translate-x-1'
                }`}
              >
                <span className={`text-lg transition-transform duration-300 ${isActive ? 'scale-110' : 
  'group-hover:scale-110'}`}>
                  {item.icon}
                </span>
                <span className="font-semibold">{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-[#334155]">
          <div className="flex items-center gap-3 px-3 py-2 bg-[#1E3A5F] rounded-lg">
            <div className="w-8 h-8 bg-gradient-to-br from-[#10B981] to-[#059669] rounded-full flex
  items-center justify-center text-white font-bold text-sm shadow">
              A
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-white">Admin User</p>
              <p className="text-xs text-[#94A3B8]">System Operator</p>
            </div>
          </div>
        </div>
      </div>
    );
  }