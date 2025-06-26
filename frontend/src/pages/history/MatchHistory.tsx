import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import axios from "axios";

interface Match {
  tournament_name: string;
  opponent: string;
  result: string; // "win" or "loss"
  date: string;
}

const MatchHistory = () => {
  const { user } = useAuth();
  const [matches, setMatches] = useState<Match[]>([]);

  useEffect(() => {
    if (user) {
      axios.get(`/matches/user/${user.username}`).then(res => {
        setMatches(res.data);
      });
    }
  }, [user]);

  return (
    <div style={{ padding: "1rem" }}>
      <h2>Match History</h2>
      {matches.length === 0 ? (
        <p>No matches found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Tournament</th>
              <th>Opponent</th>
              <th>Result</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((m, i) => (
              <tr key={i}>
                <td>{new Date(m.date).toLocaleDateString()}</td>
                <td>{m.tournament_name}</td>
                <td>{m.opponent}</td>
                <td style={{ color: m.result === "win" ? "green" : "red" }}>{m.result}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MatchHistory;
