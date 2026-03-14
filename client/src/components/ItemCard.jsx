import { Link } from "react-router-dom"

function ItemCard({ item }){

  return(

    <div
      style={{
        width:"230px",
        border:"1px solid #ddd",
        borderRadius:"10px",
        overflow:"hidden",
        background:"#fff",
        boxShadow:"0 2px 8px rgba(0,0,0,0.1)",
        transition:"transform 0.2s"
      }}
    >

      <img
        src={item.photo || "https://via.placeholder.com/200"}
        alt={item.title}
        style={{
          width:"100%",
          height:"160px",
          objectFit:"cover"
        }}
      />

      <div style={{padding:"10px"}}>

        <h3>{item.title}</h3>

        <p style={{color:"#777"}}>{item.category}</p>

        <p style={{fontSize:"14px"}}>{item.location}</p>

        <Link to={`/item/${item.id}`}>
          <button
            style={{
              marginTop:"8px",
              width:"100%",
              padding:"6px",
              background:"#3498db",
              color:"white",
              border:"none",
              borderRadius:"5px"
            }}
          >
            View Item
          </button>
        </Link>

      </div>

    </div>

  )

}

export default ItemCard 