import { createContext, useContext, useEffect, useState } from 'react';
import client from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const access = localStorage.getItem('access_token');
    if (!access) {
      setLoading(false);
      return;
    }
    client
      .get('/api/auth/me/')
      .then(({ data }) => setUser(data))
      .catch(() => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
      })
      .finally(() => setLoading(false));
  }, []);

  async function login(username, password) {
    const { data } = await client.post('/api/auth/login/', { username, password });
    localStorage.setItem('access_token', data.access);
    localStorage.setItem('refresh_token', data.refresh);
    const me = await client.get('/api/auth/me/');
    setUser(me.data);
  }

  async function register(username, email, password) {
    await client.post('/api/auth/register/', { username, email, password });
    await login(username, password);
  }

  function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
