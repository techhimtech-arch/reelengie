import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Step1Details from '../components/wizard/Step1Details';
import Step2Script from '../components/wizard/Step2Script';
import Step3Voice from '../components/wizard/Step3Voice';
import Step4Media from '../components/wizard/Step4Media';

const NewProject = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [projectId, setProjectId] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleNext = () => setCurrentStep(prev => Math.min(prev + 1, 5));
  const handleBack = () => setCurrentStep(prev => Math.max(prev - 1, 1));
  const handleCancel = () => navigate('/dashboard');

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto">
      <header className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Create New Reel</h2>
        <div className="flex items-center gap-2 text-textMuted text-sm">
          <span className={currentStep >= 1 ? "text-primary font-bold" : ""}>Details</span> &gt;
          <span className={currentStep >= 2 ? "text-primary font-bold" : ""}>Script</span> &gt;
          <span className={currentStep >= 3 ? "text-primary font-bold" : ""}>Voice</span> &gt;
          <span className={currentStep >= 4 ? "text-primary font-bold" : ""}>Media</span>
        </div>
      </header>

      <div className="flex-1 glass-panel p-8 flex flex-col relative overflow-hidden">
        {currentStep === 1 && <Step1Details onNext={handleNext} setProjectId={setProjectId} />}
        {currentStep === 2 && <Step2Script onNext={handleNext} onBack={handleBack} projectId={projectId} />}
        {currentStep === 3 && <Step3Voice onNext={handleNext} onBack={handleBack} projectId={projectId} />}
        {currentStep === 4 && <Step4Media onNext={() => navigate('/dashboard')} onBack={handleBack} projectId={projectId} />}
      </div>
    </div>
  );
};

export default NewProject;
