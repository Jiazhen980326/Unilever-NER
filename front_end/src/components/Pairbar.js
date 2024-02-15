import './Pairbar.css'

export default function Pairbar( {pairs, clickPair, clickRelation, confirmation, confirming} ) {
  return (
    <div className="column">
    <h1 className='lower-title'>Pairs</h1>
    <div className='scroll-bar'>
      {pairs.map((pair) => (
        <div className='row' key={pair.h.id*1000+pair.t.id}>
          <div className="column-noshadow left">
            <div className="pair-box pair-text" onClick={() => {clickPair(pair)}} style={{
          borderColor: confirmation.has(pair.id)? "#1ab5ed": "#58249c" }}>
              <p>{pair.h.text} -{'>'} {pair.t.text}</p>
            </div>
          </div>
          <div className="column-noshadow middle">
            <p className="dashline">-----{'>'}</p>
          </div>
          <div className="column-noshadow right">
            <div className="pair-box pair-rel" onClick={() => {clickRelation(pair.relation, pair.id)}} style={{
          borderColor: (confirmation.has(pair.id) && confirming !== pair.id)? "#1ab5ed": "#58249c" }}>
              <p>{(confirmation.has(pair.id) && confirming !== pair.id)? confirmation.get(pair.id)['relation']: pair.relation}</p>
            </div>
          </div>
        </div>
      ))}
    </div>
    </div>
  )
}