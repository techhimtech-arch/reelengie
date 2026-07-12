import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import Preview from './pages/Preview';

import NewProject from './pages/NewProject';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="new" element={<NewProject />} />
          <Route path="project/:id/preview" element={<Preview />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
