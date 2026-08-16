import React, { useEffect, useState } from "react";
import { getProfile } from "../services/api";

function Dashboard() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchProfile = async () => {
      const res = await getProfile();
      setData(res);
    };

    fetchProfile();
  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Dashboard</h2>

      {data ? (
        <p>{data.message}</p>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default Dashboard;