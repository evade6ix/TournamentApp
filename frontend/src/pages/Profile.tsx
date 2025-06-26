import { useAuth } from "../context/AuthContext";
import { Link } from "react-router-dom";

const Profile = () => {
  const { user } = useAuth();

  if (!user) return <div>Not logged in</div>;

  return (
    <div style={{ padding: "1rem" }}>
      <h1>{user.username}'s Profile</h1>
      {user.is_admin && <p style={{ color: "red" }}>🛡️ ADMIN</p>}
      <img
        src={user.profile_picture || "/default-avatar.png"}
        alt="Profile"
        width={120}
        style={{ borderRadius: "50%", marginTop: "1rem" }}
      />
      <Link to="/profile/edit">Edit Profile</Link>
      <p>Email: {user.email}</p>
      <p>Bio: {user.bio || "No bio set."}</p>
    </div>
  );
};

export default Profile;
