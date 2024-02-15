/* eslint-disable */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'

import Navbar from './components/Navbar'
import Annotate from './pages/Annotate'
import List from './pages/List'
import Input from './pages/Input'

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Navbar />
        <Routes>
          <Route path="/input" element={<Input />} />
          <Route path="/list" element={<List />} />
          <Route path="/annotate/:id" element={<Annotate />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
