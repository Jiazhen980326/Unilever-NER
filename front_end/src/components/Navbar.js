import React from 'react'
import './Navbar.css'
import { Link } from 'react-router-dom'
// import SearchBar from './SearchBar'

export default function Navbar() {
  return (
    <div className="navbar">
        <nav>
            <Link to="/" className="brand">
                <h1>Annotation Website</h1>
            </Link>
            <Link to="/input" className="switch">Input</Link>
            <Link to="/list" className='switch'>Index</Link>
            <Link to="/annotate" className='switch'>Annotate</Link>
        </nav>
    </div>
  )
}
