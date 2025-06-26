import { Link } from "react-router-dom"

const Navbar = () => {
  return (
    <nav style={{ padding: "1rem", background: "#222", color: "#fff" }}>
      <ul style={{ display: "flex", gap: "1rem", listStyle: "none" }}>
        <li><Link to="/" style={{ color: "white", textDecoration: "none" }}>Home</Link></li>
        <li><Link to="/dashboard" style={{ color: "white", textDecoration: "none" }}>Dashboard</Link></li>
        <li><Link to="/login" style={{ color: "white", textDecoration: "none" }}>Login</Link></li>
        <li><Link to="/register" style={{ color: "white", textDecoration: "none" }}>Register</Link></li>
      </ul>
    </nav>
  )
}

export default Navbar
