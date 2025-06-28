import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import WaterSystemReport from './pages/WaterSystemReport';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/report/:pwsid" element={<WaterSystemReport />} />
      </Routes>
    </Router>
  )
}

export default App
