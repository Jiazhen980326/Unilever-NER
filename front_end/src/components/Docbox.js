import { useFetch } from "../hooks/useFetch"
import configData from "../config.json"
import './Docbox.css'

export default function Docbox( {data, id, setData} ) {
  const { postData } = useFetch(`${configData.SERVER_URL}new_entity`, 'POST')
  const handleEntitySelection = (e) => {
    e.preventDefault()
    let newEntity = window.getSelection().toString()
    if (newEntity.length !== 0) {
      postData({ "text": newEntity, "doc_id": id })
      window.location.reload(false)
    }
  }

  return (
    <>
    <div className="docbox-column">
      <h1 className='docbox-title'>Document</h1>
        <div className="docbox"><p>{data.text}</p></div>
        <form onSubmit={(e)=>handleEntitySelection(e)}>
        <button className="btn">Add Entity</button>
      </form>
    </div>
    </>
  )
}