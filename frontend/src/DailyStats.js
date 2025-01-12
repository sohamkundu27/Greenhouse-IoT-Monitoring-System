import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const DailyStats = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStats = () => {
            axios
                .get("http://localhost:8000/api/daily-stats/")
                .then(response => {
                    setStats(response.data); // Save the backend response to state
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Error fetching daily stats:", err);
                    setError("Failed to fetch daily stats.");
                    setLoading(false);
                });
        };

        fetchStats();
    }, []);

    return (
        <div className="dashboard">
            <h1 className="dashboard-title">Daily High/Low Stats</h1>

            {loading ? (
                <p>Loading daily stats...</p>
            ) : error ? (
                <p className="error-message">{error}</p>
            ) : stats ? (
                <div className="stats-container">
                    <div className="stats-header">
                        <div className="sensor-item">Date</div>
                        <div className="sensor-item">Max Temperature</div>
                        <div className="sensor-item">Min Temperature</div>
                        <div className="sensor-item">Max Humidity</div>
                        <div className="sensor-item">Min Humidity</div>
                    </div>
                    <div className="stats-row">
                        <div className="sensor-item">{stats.date || "N/A"}</div>
                        <div className="sensor-item">{stats.max_temperature ?? "N/A"}°C</div>
                        <div className="sensor-item">{stats.min_temperature ?? "N/A"}°C</div>
                        <div className="sensor-item">{stats.max_humidity ?? "N/A"}%</div>
                        <div className="sensor-item">{stats.min_humidity ?? "N/A"}%</div>
                    </div>
                </div>
            ) : (
                <p>No stats available for today.</p>
            )}

            <div className="button-container">
                <Link to="/">
                    <button className="back-button">Back to Dashboard</button>
                </Link>
            </div>
        </div>
    );
};

export default DailyStats;