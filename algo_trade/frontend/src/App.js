import React, { useState, useEffect } from 'react';
import axios from 'axios';
import TradeForm from './components/TradeForm';
import PositionsTable from './components/PositionsTable';
import './App.css';

function App() {
    const [positions, setPositions] = useState([]);

    const fetchPositions = async () => {
        try {
            const response = await axios.get('/positions/');
            setPositions(response.data);
        } catch (error) {
            console.error('Error fetching positions:', error);
            window.alert('Error fetching positions. Please try again later.');
        }
    };

    useEffect(() => {
        fetchPositions();
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>Trading App</h1>
            </header>
            <main>
                <TradeForm fetchPositions={fetchPositions} />
                <PositionsTable positions={positions} />
            </main>
        </div>
    );
}

export default App;
