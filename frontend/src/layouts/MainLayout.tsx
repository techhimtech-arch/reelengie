import React from 'react';
import { Outlet } from 'react-router-dom';
import { Film, Settings, FolderOpen, Video } from 'lucide-react';

const MainLayout = () => {
  return (
    <div className="flex h-screen w-screen overflow-hidden">
      {/* Sidebar Navigation */}
      <nav className="w-20 md:w-64 bg-surface border-r border-white/5 flex flex-col items-center md:items-start py-8">
        <div className="flex items-center gap-3 px-0 md:px-6 mb-12">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center shadow-glow">
            <Film className="w-5 h-5 text-white" />
          </div>
          <h1 className="hidden md:block text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-white/70">
            Reel Engine
          </h1>
        </div>
        
        <div className="flex flex-col gap-4 w-full px-2 md:px-4">
          <NavItem icon={<FolderOpen />} label="Projects" active />
          <NavItem icon={<Video />} label="Templates" />
          <div className="flex-grow"></div>
          <NavItem icon={<Settings />} label="Settings" />
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col relative overflow-hidden bg-background">
        {/* Ambient Background Glow */}
        <div className="absolute top-[-20%] right-[-10%] w-[600px] h-[600px] bg-hero-glow rounded-full blur-[120px] opacity-30 pointer-events-none"></div>
        
        <div className="flex-1 overflow-y-auto p-8 z-10 relative">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

const NavItem = ({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) => {
  return (
    <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-300 ${active ? 'bg-primary/20 text-primary border border-primary/30' : 'text-textMuted hover:text-white hover:bg-white/5 border border-transparent'}`}>
      <span className="flex-shrink-0">{icon}</span>
      <span className="hidden md:block font-medium">{label}</span>
    </button>
  );
};

export default MainLayout;
