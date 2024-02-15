import React, { useState, useEffect } from 'react'
import { useFetch } from "../hooks/useFetch"
import { useNavigate } from 'react-router-dom'
import configData from "../config.json"
import InputBlock from '../components/Inputblock'
import Currentinput from '../components/Currentinput'
import "./Input.css"

export default function Input() {
  const [constr, setConstr] = useState('mongodb://cosmosdbcolumbiacapstonefall2022:kKsp8yiihEsCiPsMLol8U27LVWD1kVzmMe1yfpknkOxkYOCTApL8ceYZwy1uMXmLd4j1k7q7yYQkxz0WpSXXyw==@cosmosdbcolumbiacapstonefall2022.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@cosmosdbcolumbiacapstonefall2022@')
  const [dbname, setDBName] = useState('pubmed')
  const [collection, setCollection] = useState('abstracts')
  const [idField, setIDField] = useState('_id')
  const [docField, setDocField] = useState('text')
  const { data, setData, isPending, error } = useFetch(`${configData.SERVER_URL}input_page`)
  
  const { postData } = useFetch(`${configData.SERVER_URL}input_page`, 'POST')
  const navigate = useNavigate()
  const handleSubmit = (e) => {
    e.preventDefault()
    postData({ "constr": constr, "dbname": dbname, "collection": collection, "idField": idField, "docField": docField })
    setData({ "constr": constr, "dbname": dbname, "collection": collection, "idField": idField, "docField": docField })
    setConstr('')
    setDBName('')
    setCollection('')
    setIDField('')
    setDocField('')
    navigate(`/input`)
  }

  return (
    <div>
      {isPending && <div>Loading...</div>}
      {error && <div>{error}</div>}
      {data && <Currentinput data={data} />}
      
    <div className='create'>
      <h2 className='page-title'>Input from MongoDB</h2>
      <form onSubmit={(e)=>handleSubmit(e)}>
        <InputBlock name='Connection String' handleChange={setConstr} state={constr} />

        <InputBlock name="Database Name" handleChange={setDBName} state={dbname} />

        <InputBlock name="Collection Name" handleChange={setCollection} state={collection} />

        <InputBlock name="Id Field" handleChange={setIDField} state={idField} />

        <InputBlock name="Document Field" handleChange={setDocField} state={docField} />
        <button className="btn">Submit</button>
      </form>
    </div>
    </div>
  )
}