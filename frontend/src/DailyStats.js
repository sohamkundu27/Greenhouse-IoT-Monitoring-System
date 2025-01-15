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

    

                <div className="stats-container">
                    <div className="stats-header">
                        <div className="sensor-item">Date</div>
                        <div className="sensor-item">Max Temperature</div>
                        <div className="sensor-item">Min Temperature</div>
                        <div className="sensor-item">Max Humidity</div>
                        <div className="sensor-item">Min Humidity</div>
                    </div>
                    <div className="stats-row">
                        <div className="sensor-item">1-13-25</div>
                        <div className="sensor-item">71°F</div>
                        <div className="sensor-item">67°C</div>
                        <div className="sensor-item">40%</div>
                        <div className="sensor-item">35%</div>
                    </div>
                </div>


            <div className="button-container">
                <Link to="/">
                    <button className="back-button">Back to Dashboard</button>
                </Link>
            </div>
        </div>
    );
};

export default DailyStats;