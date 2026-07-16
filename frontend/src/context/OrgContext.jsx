import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import client from '../api/client';
import { useAuth } from './AuthContext';

const OrgContext = createContext(null);

export function OrgProvider({ children }) {
  const { user } = useAuth();
  const [organizations, setOrganizations] = useState([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    if (!user) {
      setOrganizations([]);
      setLoading(false);
      return;
    }
    setLoading(true);
    const { data } = await client.get('/api/orgs/');
    setOrganizations(data);
    setLoading(false);
  }, [user]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <OrgContext.Provider value={{ organizations, loading, refresh }}>
      {children}
    </OrgContext.Provider>
  );
}

export function useOrgs() {
  return useContext(OrgContext);
}
