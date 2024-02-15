import { useFetch } from "../hooks/useFetch"
import configData from "../config.json"
import InputBlock from "./Inputblock"

export default function Currentinput( { data } ) {
  const fields = [
    ["constr", "Connection String"], 
    ["dbname", "Database Name"], 
    ["collection", "Collection Name"], 
    ["idField", "Id Field"],
    ["docField", "Document Field"]
  ]
  // console.log(Array.from(data))
  return (
    <div>
    <div className='create'>
      <h2 className='page-title'>Current Input</h2>
        <form>

        {fields.map(field => (
          <label key={field[0]}>
            <span>{field[1]}:</span>
            <input
              type="text"
              value={data[field[0]]}
              disabled />
          </label>
        ))}
      </form>
    </div>
    </div>
  )
}