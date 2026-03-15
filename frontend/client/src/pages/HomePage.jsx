import { useEffect, useState } from "react"
import { fetchItems } from "../api/items"
import FilterBar from "../components/FilterBar"
import SearchBar from "../components/SearchBar"
import ItemCard from "../components/ItemCard"

function HomePage(){

  const [items,setItems] = useState([])
  const [filteredItems,setFilteredItems] = useState([])
  const [loading,setLoading] = useState(true)

  useEffect(()=>{

    fetchItems().then(data=>{
      setItems(data)
      setFilteredItems(data)
      setLoading(false)
    })

  },[])


  function handleFilter(filters){

    let result = items

    if(filters.category){
      result = result.filter(item => item.category === filters.category)
    }

    if(filters.location){
      result = result.filter(item =>
        item.location.toLowerCase().includes(filters.location.toLowerCase())
      )
    }

    setFilteredItems(result)

  }


  function handleSearch(query){

    if(!query){
      setFilteredItems(items)
      return
    }

    const result = items.filter(item =>
      item.title.toLowerCase().includes(query.toLowerCase())
    )

    setFilteredItems(result)

  }


  if(loading){

    return(

      <div style={{padding:"30px", textAlign:"center"}}>

        <h2>Loading items...</h2>

      </div>

    )

  }


  return(

    <div style={{padding:"30px"}}>

      <h1 style={{marginBottom:"20px"}}>Available Items</h1>

      <SearchBar onSearch={handleSearch} />

      <FilterBar onFilter={handleFilter} />

      {filteredItems.length === 0 ? (

        <div
          style={{
            marginTop:"40px",
            textAlign:"center",
            color:"#666"
          }}
        >

          <h2>No items available yet</h2>
          <p>Be the first to post something!</p>

        </div>

      ) : (

        <div
          style={{
            display:"grid",
            gridTemplateColumns:"repeat(auto-fill, minmax(230px,1fr))",
            gap:"20px",
            marginTop:"30px"
          }}
        >

          {filteredItems.map(item => (

            <ItemCard key={item.id} item={item}/>

          ))}

        </div>

      )}

    </div>

  )

}

export default HomePage 