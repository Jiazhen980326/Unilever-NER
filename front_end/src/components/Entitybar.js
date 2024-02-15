import './Entitybar.css'

export default function Entitybar( {entities, clickEntity, entityA, entityB} ) {
  var uniqueEntities = [...new Set(entities.map(item => item.text))]
  return (
    <div className="column">
    <h1 className='lower-title'>Entities</h1>
    <div className='scroll-bar'>
      {uniqueEntities.map((entity) => (
        <div className="tagbox" key={entity} onClick={() => {clickEntity(entity)}} style={{
          borderColor: (entity===entityA || entity===entityB)
          ?"#1ab5ed": "#58249c" }}>
          <p>{entity}</p>
        </div>
      ))}
    </div>
    </div>
  )
}