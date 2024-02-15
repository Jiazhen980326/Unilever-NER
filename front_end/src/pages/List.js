import { useFetch } from "../hooks/useFetch"
import DocList from '../components/DocList'
import configData from "../config.json"

export default function List() {
  const { data, isPending, error } = useFetch(`${configData.SERVER_URL}index_page`)
  return (
    <div className='home'>
      {isPending && <div>Loading...</div>}
      {error && <div>{error}</div>}
      {data && <DocList documents={data.data} />}
    </div>
  )
}