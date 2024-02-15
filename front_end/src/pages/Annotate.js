import { useParams, useSearchParams } from "react-router-dom"
import { useState } from 'react'

import { useFetch } from "../hooks/useFetch"
import Docbox from "../components/Docbox"
import Entitybar from "../components/Entitybar"
import Pairbar from "../components/Pairbar"
import Relationbar from "../components/Relationbar"
import ConfirmSel from "../components/ConfirmSel"
import configData from "../config.json"

export default function Annotate() {
  const [searchParams, setSearchParams] = useSearchParams()
  const { id } = useParams()
  const entityA = searchParams.get("entityA")
  const entityB = searchParams.get("entityB")
  const [confirmation, setConfirmation] = useState(new Map())
  const [confirming, setConfirming] = useState(null)

  const deleteConfirm = (key) => {
    setConfirmation((prev) => {
      const newState = new Map(prev)
      newState.delete(key)
      return newState
    })
  }

  const upsert = (key, value) => {
    setConfirmation((prev) => new Map(prev).set(key, value))
  }

  let search = ""
  if (entityA) {
    search += `entityA=${entityA}`
  }
  if (entityB) {
    search += `&entityB=${entityB}`
  }
  if (search.length > 0) {
    search = "?" + search
  }

  const clickEntity = (entity) => {
    if (entityA === entity) {
      setSearchParams({ entityB, entityA: null })
    } else if (entityB === entity) {
      setSearchParams({ entityA, entityB: null })
    } else if (!entityA || entityA === 'null') {
      setSearchParams({ entityB, entityA: entity })
    } else if (!entityB || entityB === 'null') {
      setSearchParams({ entityA, entityB: entity })
    } else {
      console.log(5, entityA, entityB, entity)
    }
  }

  const clickPair = (pair) => {
    if (confirming !== null) { // if we are confirming a pair, click pair means we want to delete sth
      deleteConfirm(pair.id)
      if (confirming === pair.id) {
        setConfirming(null)
      }
    } else { // else, means we want to confirm the pair we clicked or delete a previous pair)
      if (confirmation.has(pair.id)) {
        deleteConfirm(pair.id)
      } else {
        setConfirmation(prev => new Map([...prev, [pair.id, {
            'h': pair.h.text, 
            't': pair.t.text, 
            'relation': null}]]))
        setConfirming(pair.id)
      }
    }
  }

  const clickRelation = (relation, pairid) => {
    if (confirming !== null) {
      let rel = (confirmation.has(pairid) && confirming !== pairid)? confirmation.get(pairid): relation
      let oldVal = confirmation.get(confirming)
      oldVal['relation'] = rel
      upsert(confirming, oldVal)
      setConfirming(null)
    }
  }
  // console.log(confirming)
  // console.log(confirmation)

  const { data, isPending, error, setData } = useFetch(`${configData.SERVER_URL}annotation_page/${id}${search}`)
  return (
    <div className='row'>
      {isPending && <div>Loading...</div>}
      {error && <div>{error}</div>}
      {data && <Docbox data={data} id={id} setData={setData} />}
      {/* {data.entities && <p>data.entities</p>} */}
      {data && <Entitybar entities={data.entities} clickEntity={clickEntity} entityA={entityA} entityB={entityB}/>}
      {data && <Pairbar pairs={data.relations} clickPair={clickPair} clickRelation={clickRelation} confirmation={confirmation} confirming={confirming}/>}
      {/* This way might cause the low performance cause everytime the entire pairbar is rerendered, maybe change it in someway */}
      {data && <Relationbar entities={[]} />}
      {data && <ConfirmSel 
        confirmation={confirmation} 
        confirming={confirming} 
        id={id} 
        setConfirmation={setConfirmation}
        setConfirming={setConfirming}/>}
    </div>
  )
}