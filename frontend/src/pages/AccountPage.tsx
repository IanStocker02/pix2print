import React, { useEffect, useState } from "react";
import axios from "axios";

const AccountPage = () => {
    const [accountData, setAccountData] = useState<any>(null);
    const token = localStorage.getItem("token");

    useEffect(() => {
        const fetchAccountInfo = async () => {
            try {
                const response = await axios.get("http://localhost:5000/auth/protected", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setAccountData(response.data);
            } catch (error) {
                console.error("Failed to fetch account info:", error);
            }
        };

        fetchAccountInfo();
    }, [token]);

    if (!accountData) {
        return <p>Loading account information...</p>;
    }

    return (
        <div>
            <h1>Account Information</h1>
            <p>Username: {accountData.username}</p>
            {/* Add more fields as needed */}
        </div>
    );
};

export default AccountPage;
