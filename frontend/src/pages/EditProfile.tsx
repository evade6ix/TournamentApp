import { useAuth } from "../context/AuthContext";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const EditProfile = () => {
  const { user, login } = useAuth();
  const [username, setUsername] = useState(user?.username || "");
  const [bio, setBio] = useState(user?.bio || "");
  const [file, setFile] = useState<File | null>(null);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", username);
    formData.append("bio", bio);
    if (file) formData.append("profile_picture", file);

    await axios.put("/users/me", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    await login(localStorage.getItem("token")!);
    navigate("/profile");
  };

  return (
    <form onSubmit={handleSubmit} style={{ padding: "1rem" }}>
      <h2>Edit Your Profile</h2>
      <label>Username:</label>
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
      /><br /><br />

      <label>Bio:</label><br />
      <textarea
        value={bio}
        onChange={(e) => setBio(e.target.value)}
      /><br /><br />

      <label>Profile Picture:</label><br />
      <input
        type="file"
        accept="image/*"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      /><br /><br />

      <button type="submit">Save Changes</button>
    </form>
  );
};

export default EditProfile;
