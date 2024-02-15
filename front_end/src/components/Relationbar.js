import './Entitybar.css'
import './Relationbar.css'
export default function Entitybar( {entities} ) {
  var uniqueEntities = [...new Set(entities.map(item => item.text))]

  return (
    <div className="column">
    <h1 className='lower-title'>Relations</h1>
    <div className='scroll-bar relation-bottom'>
      {uniqueEntities.map((entity) => (
        <div className="tagbox">
          <p>{entity}</p>
        </div>
      ))}
      <div className='bottom-right'>
      <div className='flex-wrapper'>
        <input id="relationInput" type="text" name="relationInput"
        placeholder="input the text" className='relation-input'/>
        <button className='btn btn-primary'>Submit</button>
      </div>
      </div>
    </div>
    </div>
  )
}