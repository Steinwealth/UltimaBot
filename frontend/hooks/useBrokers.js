import { useState } from 'react';

export default function useBrokers() {
  const [brokers, setBrokers] = useState([]);

  const addBroker = (brokerData) => {
    const newBroker = {
      id: `BROKER-${Date.now()}`,
      name: brokerData.name || 'Broker',
      key: brokerData.key,
      secret: brokerData.secret,
      pairedModel: null,
      account: {
        balance: 0,
        margin: 0,
      },
    };
    setBrokers((prev) => [...prev, newBroker]);
  };

  const pairModel = (brokerId, model) => {
    setBrokers((prev) =>
      prev.map((b) =>
        b.id === brokerId ? { ...b, pairedModel: model } : b
      )
    );
  };

  const updateAccount = (brokerId, accountData) => {
    setBrokers((prev) =>
      prev.map((b) =>
        b.id === brokerId ? { ...b, account: accountData } : b
      )
    );
  };

  const removeBroker = (brokerId) => {
    setBrokers((prev) => prev.filter((b) => b.id !== brokerId));
  };

  return {
    brokers,
    addBroker,
    pairModel,
    updateAccount,
    removeBroker,
  };
}
