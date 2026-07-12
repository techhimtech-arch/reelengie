import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Play, Loader2 } from 'lucide-react';
import { TimelineEditor } from '../components/TimelineEditor';

interface TimelineClip {
  scene: string;
  start: number;
  end: number;
  media: string;
  media_type: string;
}

const Preview = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [timeline, setTimeline] = useState<TimelineClip[]>([]);
  const [loading, setLoading] = useState(true);
  const [rendering, setRendering] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Generate/fetch the timeline
    fetch(`http://127.0.0.1:8765/api/projects/${id}/timeline`, { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'success') {
          setTimeline(data.timeline);
        } else {
          setError(data.detail || 'Failed to generate timeline');
        }
      })
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);



  const handleRender = async () => {
    setRendering(true);
    try {
      const res = await fetch(`http://127.0.0.1:8765/api/projects/${id}/render`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ timeline })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || 'Render failed');
      alert('Generation Complete! Check your project output folder.');
      navigate('/dashboard');
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setRendering(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <Loader2 className="w-12 h-12 text-primary animate-spin mb-4" />
        <h2 className="text-xl text-white">Analyzing audio and generating timeline...</h2>
        <p className="text-textMuted mt-2">This may take a few moments.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-6 rounded-xl max-w-lg text-center">
          <h2 className="text-xl font-bold mb-2">Timeline Error</h2>
          <p>{error}</p>
          <button onClick={() => navigate('/dashboard')} className="mt-4 btn-primary bg-red-500 hover:bg-red-600">Go Back</button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto pb-20">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Preview & Tweak Timeline</h2>
        <p className="text-textMuted">Reorder clips to your liking before generating the final reel.</p>
      </header>

      <div className="mb-8">
        <TimelineEditor timeline={timeline} setTimeline={setTimeline} projectId={id!} />
      </div>

      <div className="flex justify-between items-center">
        <button onClick={() => navigate('/dashboard')} className="btn-secondary">
          Cancel
        </button>
        <button 
          onClick={handleRender}
          disabled={rendering}
          className="btn-primary flex items-center gap-2 px-8 py-4 text-lg"
        >
          {rendering ? (
            <><Loader2 className="w-6 h-6 animate-spin" /> Rendering Reel...</>
          ) : (
            <><Play className="w-6 h-6" /> Render Final Reel</>
          )}
        </button>
      </div>
    </div>
  );
};

export default Preview;
