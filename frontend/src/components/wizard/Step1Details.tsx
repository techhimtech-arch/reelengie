import React, { useState } from 'react';

const Step1Details = ({ onNext, setProjectId }: { onNext: () => void, setProjectId: (id: string) => void }) => {
  const [name, setName] = useState('');
  const [treeName, setTreeName] = useState('');
  const [dayNumber, setDayNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const response = await fetch('http://127.0.0.1:8765/api/projects/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, tree_name: treeName, day_number: parseInt(dayNumber) || 0 })
      });
      const data = await response.json();
      
      if (!response.ok) throw new Error(data.detail || 'Failed to create project');
      
      setProjectId(data.id);
      onNext();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col h-full">
      <div className="flex-1 space-y-6">
        <div>
          <label className="block text-sm font-medium text-textMuted mb-2">Project Name</label>
          <input required type="text" className="input-field" placeholder="e.g. Bamboo Plantation Series" value={name} onChange={e => setName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium text-textMuted mb-2">Tree Name</label>
          <input required type="text" className="input-field" placeholder="e.g. Bamboo" value={treeName} onChange={e => setTreeName(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm font-medium text-textMuted mb-2">Day Number</label>
          <input required type="number" className="input-field" placeholder="e.g. 1" value={dayNumber} onChange={e => setDayNumber(e.target.value)} />
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
      </div>
      <div className="flex justify-end pt-6 mt-6 border-t border-white/10">
        <button type="submit" disabled={loading} className="btn-primary w-32">
          {loading ? 'Creating...' : 'Next'}
        </button>
      </div>
    </form>
  );
};

export default Step1Details;
