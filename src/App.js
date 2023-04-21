import logo from './logo.svg';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ResponsiveAppBar from './components/navigationbar.js'
import Payouts from './pages/payouts.js'
import Reporting from './pages/reports.js'

function App() {
  return (
    <Router>
      <div className="App">
        <ResponsiveAppBar />
        <div className='content'>
          <Routes>
            <Route exact path='/' element={<Payouts/>}/>
            <Route exact path='/reporting' element={<Reporting/>}/>
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;