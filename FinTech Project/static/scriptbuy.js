async function buyShares(investorId, musicId, sharesToBuy) {
    const response = await fetch('/api/buy_share', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            investor_id: investorId,
            music_id: musicId,
            shares_to_buy: sharesToBuy
        })
    });

    const result = await response.json();
    if (response.ok) {
        alert(result.message);  // "Share purchased successfully!"
    } else {
        alert(result.error);    // Error message
    }
}