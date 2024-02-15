import { useFetch } from "../hooks/useFetch"
import configData from "../config.json"
import { useNavigate } from 'react-router-dom'
import "./ConfirmSel.css"

export default function ConfirmSel( {confirmation, confirming, id, setConfirmation, setConfirming} ) {
  const { postData, data } = useFetch(`${configData.SERVER_URL}annotation_page/${id}`, 'POST')
  const navigate = useNavigate()
  const handleSubmit = (e) => {
    e.preventDefault()
    postData({ "confirmed": Array.from(confirmation).filter(([key, value]) => {return value['relation'] !== null}) })
    setConfirmation((prev) => new Map(prev.clear()))
    setConfirming(null)
    navigate(`/annotate/${id}`)
  }

  return (
    <div className="confirm-column">
      <form onSubmit={(e)=>handleSubmit(e)}>
        <button className="btn" disabled={confirmation.size - (confirming !== null? 1: 0) < 1}>Submit Relations</button>
      </form>
    </div>
  )
}
