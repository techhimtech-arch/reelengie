import React, { useState } from 'react';

const Step2Script = ({ onNext, onBack, projectId }: { onNext: () => void, onBack: () => void, projectId: string | null }) => {
  const [script, setScript] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`http://127.0.0.1:8765/api/uploads/${projectId}/script`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: script })
      });
      const data = await response.json();
      
      if (!response.ok) throw new Error(data.detail || 'Failed to save script');
      onNext();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col h-full">
      <div className="flex-1 space-y-4 flex flex-col">
        <label className="block text-sm font-medium text-textMuted">Narration Script</label>
        <p className="text-xs text-textMuted/70 mb-2">Divide your script naturally. Our engine will sync this with the voice.</p>
        <textarea 
          required
          className="input-field flex-1 resize-none font-mono text-sm leading-relaxed" 
          placeholder="[Hook]&#10;Did you know bamboo grows up to 3 feet a day?&#10;&#10;[Intro]&#10;Today we are planting..."
          value={script} 
          onChange={e => setScript(e.target.value)} 
        />
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>
      <div className="flex justify-between pt-6 mt-6 border-t border-white/10">
        <button type="button" onClick={onBack} disabled={loading} className="btn-secondary w-32">Back</button>
        <button type="submit" disabled={loading} className="btn-primary w-32">
          {loading ? 'Saving...' : 'Next'}
        </button>
      </div>
    </form>
  );
};

export default Step2Script;
