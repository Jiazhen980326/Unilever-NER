import React from 'react'
import { Link } from 'react-router-dom'
import './DocList.css'

export default function DocList({documents}) {

  return (
    <div className='recipe-list'>
        {documents.map(document => (
            <div key={document._id} className='card'>
                <h3>{document._id}</h3> 
                {/* <p>{document.text}</p> */}
                <div>{document.text.substring(0, 100)}...</div>
                <Link to={`/annotate/${document._id}`}>Annotate</Link>
            </div>
        ))}
    </div>
  )
}
