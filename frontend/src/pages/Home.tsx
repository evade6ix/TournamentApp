import { Link } from "react-router-dom"

export default function Home() {
  return (
    <div className="p-6 text-center">
      <h1 className="text-3xl font-bold mb-4">Beyblade X Tournament Hub</h1>
      <p className="mb-4">Track events, players, and match history live.</p>
      <div className="space-x-4">
        <Link to="/login" className="text-blue-600 underline">Login</Link>
        <Link to="/register" className="text-green-600 underline">Register</Link>
      </div>
    </div>
  )
}
