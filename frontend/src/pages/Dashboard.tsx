import { useState, useEffect } from 'react';
import { Plus, Clock, FileVideo, Play } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<any[]>([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8765/api/projects/')
      .then(res => res.json())
      .then(data => setProjects(data))
      .catch(err => console.error(err));
  }, []);
  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto">
      <header className="flex justify-between items-end mb-10">
        <div>
          <h2 className="text-3xl font-bold text-white mb-2">Projects</h2>
          <p className="text-textMuted">Manage and generate your social media reels.</p>
        </div>
        <button onClick={() => navigate('/new')} className="btn-primary flex items-center gap-2">
          <Plus className="w-5 h-5" />
          <span>New Project</span>
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        
        {projects.map(project => (
          <div key={project.id} className="glass-panel p-6 group cursor-pointer hover:border-primary/50 transition-all duration-300">
            <div className="flex justify-between items-start mb-4">
              <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center text-primary">
                <FileVideo className="w-6 h-6" />
              </div>
              <span className="text-xs font-medium px-2 py-1 rounded-full bg-green-500/20 text-green-400 border border-green-500/20">
                {project.status || 'Draft'}
              </span>
            </div>
            <h3 className="text-xl font-semibold text-white mb-1 group-hover:text-primary transition-colors">{project.name}</h3>
            <p className="text-textMuted text-sm mb-6 flex items-center gap-1">
              <Clock className="w-4 h-4" /> {new Date(project.created_at).toLocaleDateString()}
            </p>
            <div className="flex gap-2">
              <button 
                onClick={(e) => { e.stopPropagation(); navigate(`/project/${project.id}/preview`); }}
                className="btn-primary py-2 text-sm flex-1 flex justify-center items-center gap-2"
              >
                <Play className="w-4 h-4" /> Preview & Tweak
              </button>
              <a 
                href={`http://127.0.0.1:8765/static/${project.id}/output/output.mp4`}
                target="_blank"
                rel="noopener noreferrer"
                onClick={(e) => e.stopPropagation()}
                className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded-lg text-sm flex justify-center items-center gap-2 transition-colors font-semibold"
              >
                Watch Reel
              </a>
            </div>
          </div>
        ))}
        
        {/* Empty State / Create New Card */}
        <div onClick={() => navigate('/new')} className="glass-panel p-6 border-dashed border-white/20 hover:border-primary/50 flex flex-col items-center justify-center text-center cursor-pointer transition-all duration-300 min-h-[220px]">
          <div className="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center text-textMuted mb-4">
            <Plus className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-semibold text-white mb-1">Create New Reel</h3>
          <p className="text-textMuted text-sm">Start a new automated rendering project.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
