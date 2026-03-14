import { Link } from "react-router-dom"

function Navbar(){

  const navStyle = {
    display:"flex",
    justifyContent:"space-between",
    alignItems:"center",
    padding:"15px 40px",
    background:"#2c3e50",
    color:"white"
  }

  const linksStyle = {
    display:"flex",
    gap:"20px"
  }

  const linkStyle = {
    color:"white",
    textDecoration:"none",
    fontWeight:"500"
  }

  return(

    <nav style={navStyle}>

      <h2>Declutter254</h2>

      <div style={linksStyle}>

        <Link style={linkStyle} to="/">Home</Link>

        <Link style={linkStyle} to="/post-item">Post Item</Link>

        <Link style={linkStyle} to="/profile">Profile</Link>

        <Link style={linkStyle} to="/requests">Requests</Link>

        <Link style={linkStyle} to="/login">Login</Link>

      </div>

    </nav>

  )

}

export default Navbar 