import { useEffect, useState } from "react";
import axios from "axios";

interface Player {
  username: string;
  elo: number;
  is_admin?: boolean;
}

const Leaderboard = () => {
  const [players, setPlayers] = useState<Player[]>([]);

  useEffect(() => {
    axios.get("/users/leaderboard").then(res => {
      setPlayers(res.data);
    });
  }, []);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Top Players</h2>
      <table>
        <thead>
          <tr>
            <th>Rank</th>
            <th>Username</th>
            <th>ELO</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, i) => (
            <tr key={p.username}>
              <td>{i + 1}</td>
              <td>
                {p.username} {p.is_admin && <strong style={{ color: "red" }}>(ADMIN)</strong>}
              </td>
              <td>{p.elo}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Leaderboard;
