import React, { useState, useEffect } from 'react';

const getLtp = async (symbol) => {
    // This is a placeholder function.
    // In a real application, you would call an API to get the LTP.
    // For now, we will return a mock LTP.
    console.log(`Fetching LTP for ${symbol} (mocked)`);
    // In a real app, you'd fetch this from your backend, which would then call the Angel One API
    return new Promise(resolve => setTimeout(() => resolve(Math.random() * 100 + 50), 200)); // Mock LTP with a delay
};


const PositionsTable = ({ positions }) => {
    const [ltps, setLtps] = useState({});

    useEffect(() => {
        const fetchLtps = async () => {
            const newLtps = {};
            for (const position of positions) {
                if (!ltps[position.symbol]) { // Fetch only if LTP not already present
                    const ltp = await getLtp(position.symbol);
                    newLtps[position.symbol] = ltp;
                }
            }
            setLtps(prevLtps => ({...prevLtps, ...newLtps}));
        };

        if (positions.length > 0) {
            fetchLtps();
        }
    }, [positions]);

    const calculatePnl = (position) => {
        const ltp = ltps[position.symbol] || position.average_price;
        return (ltp - position.average_price) * position.quantity;
    };

    const getUnderlyingSymbol = (symbol) => {
        // This is a simple logic to extract the underlying symbol.
        // It assumes the underlying is the first part of the symbol, consisting of uppercase letters.
        // For example, for "NIFTY 25JUL24 23500 CE", the underlying is "NIFTY".
        // You might need to adjust this logic based on your symbol format.
        const match = symbol.match(/^[A-Z&]+/);
        return match ? match[0] : symbol;
    };

    const groupedPositions = positions.reduce((acc, position) => {
        const underlying = getUnderlyingSymbol(position.symbol);
        if (!acc[underlying]) {
            acc[underlying] = [];
        }
        acc[underlying].push(position);
        return acc;
    }, {});

    const totalPnl = positions.reduce((acc, position) => acc + calculatePnl(position), 0);

    return (
        <div>
            <h2>Open Positions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Symbol</th>
                        <th>Quantity</th>
                        <th>Average Price</th>
                        <th>LTP</th>
                        <th>PnL</th>
                    </tr>
                </thead>
                <tbody>
                    {Object.entries(groupedPositions).map(([underlying, pos]) => (
                        <React.Fragment key={underlying}>
                            <tr>
                                <td colSpan="4"><strong>{underlying}</strong></td>
                                <td><strong>{pos.reduce((acc, p) => acc + calculatePnl(p), 0).toFixed(2)}</strong></td>
                            </tr>
                            {pos.map((position) => (
                                <tr key={position.id}>
                                    <td>{position.symbol}</td>
                                    <td>{position.quantity}</td>
                                    <td>{position.average_price.toFixed(2)}</td>
                                    <td>{ltps[position.symbol] ? ltps[position.symbol].toFixed(2) : 'Fetching...'}</td>
                                    <td>{ltps[position.symbol] ? calculatePnl(position).toFixed(2) : 'Calculating...'}</td>
                                </tr>
                            ))}
                        </React.Fragment>
                    ))}
                </tbody>
                <tfoot>
                    <tr>
                        <td colSpan="4"><strong>Total PnL</strong></td>
                        <td><strong>{totalPnl.toFixed(2)}</strong></td>
                    </tr>
                </tfoot>
            </table>
        </div>
    );
};

export default PositionsTable;
