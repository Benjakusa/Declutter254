import { Link } from "react-router-dom"

function ItemCard({ item }) {

  return (

    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "10px",
        overflow: "hidden",
        background: "#fff",
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
        transition: "transform 0.2s",
        cursor: "pointer"
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.03)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
    >

      <img
        src={item.photo || "https://via.placeholder.com/300"}
        alt={item.title}
        style={{
          width: "100%",
          height: "160px",
          objectFit: "cover"
        }}
      />

      <div style={{ padding: "12px" }}>

        <h3 style={{ marginBottom: "6px" }}>{item.title}</h3>

        <p style={{ color: "#777", marginBottom: "4px" }}>
          {item.category}
        </p>

        <p style={{ fontSize: "14px", marginBottom: "10px" }}>
          {item.location}
        </p>

        <Link to={`/item/${item.id}`}>
          <button
            style={{
              width: "100%",
              padding: "7px",
              background: "#3498db",
              color: "white",
              border: "none",
              borderRadius: "5px"
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