import React, { useState, useRef } from 'react';

const Step4Media = ({ onNext, onBack, projectId }: { onNext: () => void, onBack: () => void, projectId: string | null }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(prev => [...prev, ...Array.from(e.target.files as FileList)]);
    }
  };

  const uploadFile = async (file: File) => {
    const isVideo = file.type.startsWith('video/');
    const mediaType = isVideo ? 'videos' : 'photos';
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`http://127.0.0.1:8765/api/uploads/${projectId}/media/${mediaType}`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) throw new Error(`Failed to upload ${file.name}`);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (files.length === 0) return;
    
    setLoading(true);
    try {
      for (let i = 0; i < files.length; i++) {
        await uploadFile(files[i]);
        setProgress(Math.round(((i + 1) / files.length) * 100));
      }
      onNext();
    } catch (err) {
      alert(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col h-full">
      <div className="flex-1 space-y-6">
        <h3 className="text-xl font-semibold text-white">Upload Media Assets</h3>
        <p className="text-textMuted text-sm">Upload all raw videos and photos. The Timeline Engine will select and arrange them automatically.</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="glass-panel p-6 border-dashed border-2 hover:border-primary/50 cursor-pointer flex flex-col items-center justify-center text-center h-48" onClick={() => fileInputRef.current?.click()}>
            <span className="text-3xl mb-2">📸</span>
            <span className="font-semibold text-white">Select Media</span>
            <span className="text-textMuted text-sm">MP4, MOV, JPG, PNG</span>
            <input ref={fileInputRef} type="file" multiple accept="video/*,image/*" className="hidden" onChange={handleFileChange} />
          </div>
          
          <div className="glass-panel p-4 overflow-y-auto h-48">
            <h4 className="text-sm font-semibold text-textMuted mb-2 uppercase tracking-wider">Selected Files ({files.length})</h4>
            <ul className="space-y-2">
              {files.map((f, i) => (
                <li key={i} className="text-sm text-white bg-white/5 px-3 py-2 rounded flex justify-between">
                  <span className="truncate w-4/5">{f.name}</span>
                  <span className="text-textMuted">{(f.size / 1024 / 1024).toFixed(1)}MB</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {loading && (
          <div className="w-full bg-white/10 rounded-full h-2.5 mt-4">
            <div className="bg-primary h-2.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }}></div>
          </div>
        )}

      </div>
      <div className="flex justify-between pt-6 mt-6 border-t border-white/10">
        <button type="button" onClick={onBack} disabled={loading} className="btn-secondary w-32">Back</button>
        <button type="submit" disabled={files.length === 0 || loading} className="btn-primary w-40">
          {loading ? `Uploading ${progress}%` : 'Upload & Finish'}
        </button>
      </div>
    </form>
  );
};

export default Step4Media;
