import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowUp, ArrowDown, Play, Video, Image as ImageIcon, Loader2 } from 'lucide-react';

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

  const moveClip = (index: number, direction: 'up' | 'down') => {
    const newTimeline = [...timeline];
    if (direction === 'up' && index > 0) {
      const temp = newTimeline[index];
      newTimeline[index] = newTimeline[index - 1];
      newTimeline[index - 1] = temp;
    } else if (direction === 'down' && index < newTimeline.length - 1) {
      const temp = newTimeline[index];
      newTimeline[index] = newTimeline[index + 1];
      newTimeline[index + 1] = temp;
    }
    // Note: Start and End times are kept the same per index slot, just the media changes
    // Wait, the timeline array has fixed start/end times per index.
    // If we swap clips, we should only swap the media and media_type!
    // Let's swap media and media_type instead of the whole object to keep timestamps in order.
    
    const actualNewTimeline = [...timeline];
    if (direction === 'up' && index > 0) {
      const media1 = actualNewTimeline[index].media;
      const type1 = actualNewTimeline[index].media_type;
      actualNewTimeline[index].media = actualNewTimeline[index - 1].media;
      actualNewTimeline[index].media_type = actualNewTimeline[index - 1].media_type;
      actualNewTimeline[index - 1].media = media1;
      actualNewTimeline[index - 1].media_type = type1;
    } else if (direction === 'down' && index < actualNewTimeline.length - 1) {
      const media1 = actualNewTimeline[index].media;
      const type1 = actualNewTimeline[index].media_type;
      actualNewTimeline[index].media = actualNewTimeline[index + 1].media;
      actualNewTimeline[index].media_type = actualNewTimeline[index + 1].media_type;
      actualNewTimeline[index + 1].media = media1;
      actualNewTimeline[index + 1].media_type = type1;
    }
    
    setTimeline(actualNewTimeline);
  };

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

      <div className="glass-panel p-6 mb-8">
        <div className="flex flex-col gap-4">
          {timeline.map((clip, index) => (
            <div key={index} className="flex items-center gap-4 bg-white/5 border border-white/10 p-4 rounded-xl hover:border-primary/30 transition-colors">
              <div className="flex flex-col gap-1 text-textMuted">
                <button 
                  onClick={() => moveClip(index, 'up')}
                  disabled={index === 0}
                  className="p-1 hover:text-white disabled:opacity-30 disabled:hover:text-textMuted transition-colors"
                >
                  <ArrowUp className="w-5 h-5" />
                </button>
                <button 
                  onClick={() => moveClip(index, 'down')}
                  disabled={index === timeline.length - 1}
                  className="p-1 hover:text-white disabled:opacity-30 disabled:hover:text-textMuted transition-colors"
                >
                  <ArrowDown className="w-5 h-5" />
                </button>
              </div>
              
              <div className="w-24 h-24 rounded-lg bg-black/40 flex items-center justify-center flex-shrink-0 text-primary overflow-hidden">
                {clip.media_type === 'video' ? (
                  <video src={`http://127.0.0.1:8765/static/${id}/videos/${clip.media}`} className="w-full h-full object-cover" autoPlay muted loop playsInline />
                ) : (
                  <img src={`http://127.0.0.1:8765/static/${id}/photos/${clip.media}`} className="w-full h-full object-cover" alt="media" />
                )}
              </div>
              
              <div className="flex-1 min-w-0">
                <h4 className="text-white font-medium text-lg truncate">{clip.media}</h4>
                <div className="flex gap-3 text-sm text-textMuted mt-1">
                  <span className="bg-primary/20 text-primary px-2 py-0.5 rounded-full text-xs border border-primary/20">
                    {clip.scene}
                  </span>
                  <span>{clip.start.toFixed(1)}s - {clip.end.toFixed(1)}s</span>
                  <span>Duration: {(clip.end - clip.start).toFixed(1)}s</span>
                </div>
              </div>
            </div>
          ))}
        </div>
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
