import "./Inputblock.css"

export default function InputBlock({name, handleChange, state}) {
  return (
    <label>
      <span>{name}:</span>
      <input
        type="text"
        onChange={(e) => {handleChange(e.target.value)}}
        value={state}
        required />
    </label>
  )
}