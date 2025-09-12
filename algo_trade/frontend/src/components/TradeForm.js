import React, { useState } from 'react';
import axios from 'axios';

const TradeForm = ({ fetchPositions }) => {
    const [symbol, setSymbol] = useState('');
    const [quantity, setQuantity] = useState('');
    const [price, setPrice] = useState('');
    const [tradeType, setTradeType] = useState('buy');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('/trades/', {
                symbol,
                quantity: parseInt(quantity),
                price: parseFloat(price),
                trade_type: tradeType,
            });
            fetchPositions();
            setSymbol('');
            setQuantity('');
            setPrice('');
        } catch (error) {
            console.error('Error creating trade:', error);
            window.alert('Error creating trade. Please check your inputs and try again.');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <h2>Create Trade</h2>
            <div>
                <label>Symbol:</label>
                <input type="text" value={symbol} onChange={(e) => setSymbol(e.target.value)} required />
            </div>
            <div>
                <label>Quantity:</label>
                <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
            </div>
            <div>
                <label>Price:</label>
                <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} required />
            </div>
            <div>
                <label>Trade Type:</label>
                <select value={tradeType} onChange={(e) => setTradeType(e.target.value)}>
                    <option value="buy">Buy</option>
                    <option value="sell">Sell</option>
                </select>
            </div>
            <button type="submit">Create Trade</button>
        </form>
    );
};

export default TradeForm;
