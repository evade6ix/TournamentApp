import { useEffect, useState } from "react"
import axios from "axios"
import { useNavigate } from "react-router-dom"

export default function Dashboard() {
  const [user, setUser] = useState<{ username: string } | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.get("https://tournamentapp-production.up.railway.app/users/me", {
          headers: { Authorization: `Bearer ${token}` }
        })
        setUser(res.data)
      } catch (err) {
        navigate("/login")
      }
    }

    fetchUser()
  }, [])

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-2">Dashboard</h2>
      {user ? (
        <p>Welcome, {user.username}!</p>
      ) : (
        <p>Loading user info...</p>
      )}
    </div>
  )
}
