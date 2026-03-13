import { Link } from "react-router-dom"

function ItemCard({ item }) {

  return (

    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "8px",
        padding: "10px",
        width: "220px",
        background: "#fff"
      }}
    >

      <img
        src={item.photo || "https://via.placeholder.com/200"}
        alt={item.title}
        style={{
          width: "100%",
          height: "150px",
          objectFit: "cover",
          borderRadius: "5px"
        }}
      />

      <h3>{item.title}</h3>

      <p>{item.category}</p>

      <p>{item.location}</p>

      <Link to={`/items/${item.id}`}>
        <button>View Item</button>
      </Link>

    </div>

  )

}

export default ItemCard 