import axios from 'axios';

/**
 * Submits a trade to the backend trade engine.
 * @param {Object} trade - The trade object with symbol, side, size, model, TP/SL, etc.
 * @returns {Promise<Object>} - Backend response with trade ID or error.
 */
export async function submitTrade(trade) {
  try {
    const response = await axios.post('http://localhost:8000/api/trade/submit', trade);
    return {
      success: true,
      data: response.data,
    };
  } catch (error) {
    console.error('Trade submission failed:', error);
    return {
      success: false,
      error: error.response?.data || error.message,
    };
  }
}
