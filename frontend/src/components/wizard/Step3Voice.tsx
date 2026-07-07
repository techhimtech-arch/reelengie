import React, { useState } from 'react';

const Step3Voice = ({ onNext, onBack, projectId }: { onNext: () => void, onBack: () => void, projectId: string | null }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    setError('');
    
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`http://127.0.0.1:8765/api/uploads/${projectId}/media/voice`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      
      if (!response.ok) throw new Error(data.detail || 'Failed to upload voice');
      onNext();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col h-full">
      <div className="flex-1 flex flex-col items-center justify-center space-y-6">
        
        <div className="w-full max-w-md glass-panel p-8 text-center border-dashed border-2 hover:border-primary/50 transition-colors">
           <input type="file" id="voice-upload" accept="audio/mp3,audio/wav" className="hidden" onChange={handleFileChange} />
           <label htmlFor="voice-upload" className="cursor-pointer flex flex-col items-center">
             <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-4 text-primary">
               <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-8 h-8"><path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 006-6v-1.5m-6 7.5a6 6 0 01-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 01-3-3V4.5a3 3 0 116 0v8.25a3 3 0 01-3 3z" /></svg>
             </div>
             <span className="font-semibold text-lg text-white mb-2">Upload Voice Recording</span>
             <span className="text-textMuted text-sm">MP3 or WAV up to 50MB</span>
             {file && <span className="mt-4 text-green-400 text-sm font-medium">{file.name} selected</span>}
           </label>
        </div>
        
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>
      <div className="flex justify-between pt-6 mt-6 border-t border-white/10">
        <button type="button" onClick={onBack} disabled={loading} className="btn-secondary w-32">Back</button>
        <button type="submit" disabled={!file || loading} className="btn-primary w-32">
          {loading ? 'Uploading...' : 'Next'}
        </button>
      </div>
    </form>
  );
};

export default Step3Voice;
