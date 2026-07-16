import { useState } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import { useOrgs } from '../context/OrgContext';

export default function OrgListPage() {
  const { organizations, loading, refresh } = useOrgs();
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [creating, setCreating] = useState(false);

  async function handleCreate(e) {
    e.preventDefault();
    setError('');
    setCreating(true);
    try {
      await client.post('/api/orgs/', { name });
      setName('');
      await refresh();
    } catch (err) {
      setError('Could not create organization.');
    } finally {
      setCreating(false);
    }
  }

  if (loading) return <p>Loading organizations…</p>;

  return (
    <div className="page">
      <h1>Your organizations</h1>

      <ul className="org-list">
        {organizations.map((org) => (
          <li key={org.slug}>
            <Link to={`/orgs/${org.slug}/projects`}>{org.name}</Link>
            <span className="muted">
              {' '}
              — {org.my_role} · {org.member_count} member{org.member_count === 1 ? '' : 's'}
            </span>
          </li>
        ))}
      </ul>

      <form className="inline-form" onSubmit={handleCreate}>
        <input
          placeholder="New organization name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <button type="submit" disabled={creating}>
          {creating ? 'Creating…' : 'Create organization'}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}
